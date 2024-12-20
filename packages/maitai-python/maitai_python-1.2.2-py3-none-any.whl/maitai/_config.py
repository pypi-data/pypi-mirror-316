import json
import os
import threading
from typing import List

import requests
from betterproto import Casing
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from maitai._config_listener_thread import ConfigListenerThread
from maitai._utils import __version__ as version
from maitai_common.config import config_service
from maitai_gen.application import Application
from maitai_gen.config import Config as ActionConfig
from maitai_gen.key import Key, KeyMap


def _get_aws_instance_metadata(url, timeout=2):
    try:
        token_url = "http://169.254.169.254/latest/api/token"
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token_response = requests.put(token_url, headers=token_headers, timeout=timeout)

        if token_response.status_code == 200:
            token = token_response.text
            headers = {"X-aws-ec2-metadata-token": token}
        else:
            headers = None

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def _get_gcp_instance_metadata(url, timeout=2):
    try:
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def _get_azure_instance_metadata(timeout=2):
    try:
        headers = {"Metadata": "true"}
        url = "http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01"
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data.get("location")
    except requests.RequestException:
        return None


def _determine_maitai_host():
    if maitai_host := os.environ.get("MAITAI_HOST"):
        return maitai_host.rstrip("/")

    if (
        _get_aws_instance_metadata(
            "http://169.254.169.254/latest/meta-data/placement/region"
        )
        == "us-west-2"
    ):
        return "https://api.aws.us-west-2.trymaitai.ai"

    gcp_zone = _get_gcp_instance_metadata(
        "http://metadata.google.internal/computeMetadata/v1/instance/zone"
    )
    if gcp_zone:
        if "us-west1" in gcp_zone:
            return "https://api.gcp.us-west1.trymaitai.ai"
        elif "us-central1" in gcp_zone:
            return "https://api.gcp.us-central1.trymaitai.ai"

    azure_region = _get_azure_instance_metadata()
    if azure_region == "westus2":
        return "https://api.azure.westus2.trymaitai.ai"

    return "https://api.trymaitai.ai"


class Config:
    maitai_host = _determine_maitai_host()
    maitai_ws = os.environ.get(
        "MAITAI_WS", "wss://09hidyy627.execute-api.us-west-2.amazonaws.com/production"
    )
    config_dir = os.path.expanduser(os.environ.get("MAITAI_CONFIG_DIR", "~/.maitai"))

    def __init__(self):
        retry_strategy = Retry(total=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)

        self._session = requests.Session()
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

        self._api_key = None
        self._applications: dict[str, Application] = {}
        self._company_id = None
        self.websocket_listener_thread = None
        self.config_listener_thread = None
        self._application_action_configs: dict[str, dict[str, ActionConfig]] = {}
        self.initialized = False
        self.auth_keys: KeyMap = KeyMap(
            openai_api_key=Key(id=-1, key_value=os.environ.get("OPENAI_API_KEY")),
            groq_api_key=Key(id=-1, key_value=os.environ.get("GROQ_API_KEY")),
            anthropic_api_key=Key(id=-1, key_value=os.environ.get("ANTHROPIC_API_KEY")),
            cerebras_api_key=Key(id=-1, key_value=os.environ.get("CEREBRAS_API_KEY")),
        )
        self.refresh_timer = None
        self.refresh_interval = 30 * 60  # 1 hour in seconds

    @property
    def api_key(self):
        if self._api_key is None:
            if self.initialized:
                raise ValueError(
                    "Maitai API Key has not been set. Either pass it directly into the client, or by setting the environment variable MAITAI_API_KEY."
                )
            else:
                api_key = os.environ.get("MAITAI_API_KEY")
                if not api_key:
                    raise ValueError(
                        "Maitai API Key has not been set. Either pass it directly into the client, or by setting the environment variable MAITAI_API_KEY."
                    )
                self.initialize(api_key=api_key)
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def initialize(self, api_key, retry=0):
        if self.initialized and self.api_key == api_key:
            return
        self.api_key = api_key
        self.initialized = True
        try:
            self.refresh_applications()
            self._initialize_websocket()
            self._start_refresh_timer()
        except Exception as e:
            try:
                self._load_config_from_file()
            except Exception:
                raise e
            self.initialized = False
            if retry < 5:
                t = threading.Timer(
                    interval=2**retry,
                    function=self.initialize,
                    args=(api_key, retry + 1),
                )
                t.daemon = True
                t.start()

    def _start_refresh_timer(self):
        if self.refresh_timer:
            self.refresh_timer.cancel()
        self.refresh_timer = threading.Timer(
            self.refresh_interval, self._refresh_and_reschedule
        )
        self.refresh_timer.daemon = True
        self.refresh_timer.start()

    def _refresh_and_reschedule(self):
        try:
            self.refresh_applications()
        except Exception as e:
            pass
        finally:
            self._start_refresh_timer()

    def get_application(self, application_ref_name: str) -> Application:
        return self._applications.get(application_ref_name)

    def get_application_action_config(
        self, application_ref_name: str, action_type: str
    ) -> ActionConfig:
        return self._application_action_configs.get(application_ref_name, {}).get(
            action_type, config_service.get_default_config()
        )

    def refresh_applications(self):
        host = self.maitai_host
        url = f"{host}/config/init_sdk"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "x-client-version": version,
        }

        response = self._session.get(url, headers=headers, timeout=15)
        self._session.close()
        if response.status_code != 200:
            raise Exception(f"Failed to initialize Maitai client: {response.text}")
        response_json = response.json()
        applications = [
            Application().from_dict(app_json)
            for app_json in response_json["applications"]
        ]
        self._company_id = response_json.get("company_id")
        if not self._company_id:
            raise Exception("Company ID not found in response")
        return self.store_application_metadata(applications)

    def store_application_metadata(self, applications: List[Application]):
        for application in applications:
            self._applications[application.application_ref_name] = application
            for action_type in application.action_types:
                if (
                    application.application_ref_name
                    not in self._application_action_configs
                ):
                    self._application_action_configs[
                        application.application_ref_name
                    ] = {}
                self._application_action_configs[application.application_ref_name][
                    action_type.action_type
                ] = action_type.meta
        self._dump_application_metadata()

    def _dump_application_metadata(self):
        filename = os.path.join(self.config_dir, "config.json")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            config_object = {}
            for ref_name, intent_map in self._application_action_configs.items():
                config_object[ref_name] = {}
                for intent_name, intent_config in intent_map.items():
                    config_object[ref_name][intent_name] = intent_config.to_pydict(
                        casing=Casing.SNAKE, include_default_values=False
                    )
            f.write(json.dumps(config_object, indent=2))

    def _load_config_from_file(self):
        filename = os.path.join(self.config_dir, "config.json")
        with open(filename, "r") as f:
            config_object = json.load(f)
            for ref_name, intent_map in config_object.items():
                if ref_name not in self._application_action_configs:
                    self._application_action_configs[ref_name] = {}
                for intent_name, intent_config in intent_map.items():
                    self._application_action_configs[ref_name][
                        intent_name
                    ] = ActionConfig().from_pydict(intent_config)

    def _initialize_websocket(self):
        self.config_listener_thread = ConfigListenerThread(
            self, self.maitai_ws, "APPLICATION_CONFIG_CHANGE", self._company_id
        )
        self.config_listener_thread.daemon = True
        self.config_listener_thread.start()

    def cleanup(self):
        if self.config_listener_thread:
            self.config_listener_thread.terminate()
            self.config_listener_thread = None
        if self.refresh_timer:
            self.refresh_timer.cancel()
            self.refresh_timer = None


config = Config()

import atexit

atexit.register(config.cleanup)
