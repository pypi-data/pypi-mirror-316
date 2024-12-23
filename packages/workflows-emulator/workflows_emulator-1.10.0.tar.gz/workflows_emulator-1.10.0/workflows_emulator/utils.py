import importlib
import json
import os
from contextvars import copy_context
from enum import StrEnum
from threading import Thread
from typing import Optional, TypeAlias, TypedDict

import requests
import yaml
from addict import Dict as PropertyDict

STEP_NOT_FOUND = -1


class SpecialNextStep(StrEnum):
    END = 'end'
    BREAK = 'break'
    CONTINUE = 'continue'


class ParallelExceptionPolicy(StrEnum):
    CONTINUE_ALL = 'continueAll'


class RisingThread(Thread):
    """Raises inner errors in the `join` method, so they can be captured in
    the main thread"""
    exc: Exception = None
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.exc= None

    def run(self):
        try:
            super().run()
        except Exception as e:
            self.exc = e

    def join(self, timeout=None):
        super().join(timeout=timeout)
        if self.exc:
            # TODO: extract the step_id from the stacktrace
            self.exc.__context__ = RuntimeError('branch error')
            raise self.exc

class ParallelTask(TypedDict):
    id: str
    config: dict
    context: dict

class NotSet:
    pass


class ContextDict(PropertyDict):
    """
    Provides recursive access using attributes, like in javascript.
    See https://github.com/mewwts/addict?tab=readme-ov-file#default-values
    """

    def __missing__(self, key):
        raise AttributeError(key)

    def __setitem__(self, key, value):
        """If key found in the context, set it before update the dict"""
        for var in copy_context():
            if var.name == key:
                var.set(value)
        super().__setitem__(key, value)

    def __getitem__(self, item):
        """If value found in the context, set it before return it"""
        for var, value in copy_context().items():
            if var.name == item:
                return value
        return super(ContextDict, self).__getitem__(item)

    def keys(self):
        """Return a list of keys from the dict and the context"""
        dict_keys_list = list(super().keys())
        context_keys_list = [var.name for var in copy_context()]
        return dict_keys_list + context_keys_list

    def get(self, key, default=None):
        """Return the value for the key if found in the dict or the context"""
        for var, value in copy_context().items():
            if var.name == key:
                return value if value else default
        return super().get(key, default)

    def __str__(self):
        """Apparently need both, str and repr. Otherwise, some functions
        fallback to the repr, which we don't have because it is a debug
        representation and not the actual dict data"""
        return self.to_dict().__str__()

    def __repr__(self):
        """Alter the __str__ of the dict to include the contextvars tip"""
        dict_copy = self.to_dict()

        for key, value in copy_context().items():
            dict_copy[key.name + " (ContextVar)"] = value
            dict_copy.pop(key.name, None)
        return  '__repr__' + dict_copy.__repr__()


class WorkflowError(Exception):
    """Custom exception class to handle errors in workflows."""

    def __init__(self, *args, **kwargs):
        # if args is not empty, the first argument is the message
        message = ''
        if len(args) == 1:
            message = args[0]
        elif 'message' in kwargs:
            message = kwargs['message']
        super().__init__(message)
        self.payload = args[0] if args else ContextDict(kwargs)


class RuntimeError(WorkflowError):
    pass

class UnhandledBranchError(WorkflowError):
    """Custom exception class to handle errors in parallel steps."""

    def __init__(
        self,
        message: str,
        tags: list[str],
        branches: list[dict],
        truncated: bool,
        **attrs
    ):
        super().__init__(
            message=message,
            tags=tags,
            branches=branches,
            truncated=truncated,
            **attrs
        )


IMPERSONATED_SA = 'GOOGLE_CLOUD_SERVICE_ACCOUNT_NAME'
DISCOVERY_DOCUMENTS_PATH = 'discovery_documents'
DISCOVERY_DOCUMENT_URL = 'https://discovery.googleapis.com/discovery/v1/apis'
SERVICE_IDS = (
    'aiplatform:v1',
    'batch:v1',
    'bigquery:v2',
    'bigquerydatatransfer:v1',
    'cloudbuild:v1',
    'cloudfunctions:v1',
    'cloudfunctions:v2',
    'cloudresourcemanager:v1',
    'cloudresourcemanager:v2',
    'cloudresourcemanager:v3',
    'cloudscheduler:v1',
    'cloudtasks:v1',
    'compute:v1',
    'container:v1',
    'dataflow:v1b3',
    'documentai:v1',
    'firestore:v1',
    'forms:v1',
    'integrations:v1',
    'language:v1',
    'ml:v1',
    'pubsub:v1',
    'run:v1',
    'run:v2',
    'secretmanager:v1',
    'sheets:v4',
    'spanner:v1',
    'sqladmin:v1',
    'storage:v1',
    'storagetransfer:v1',
    'transcoder:v1',
    'translate:v2',
    'workflowexecutions:v1',
    'workflows:v1',
)


def get_discovery_documents(
    service_ids: list[str] = SERVICE_IDS,
    download_path: str = DISCOVERY_DOCUMENTS_PATH,
):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    main_discovery_config = requests.get(DISCOVERY_DOCUMENT_URL).json()
    service_discovery_urls = [
        service['discoveryRestUrl']
        for service in main_discovery_config['items']
        if service['id'] in service_ids
    ]

    for discovery_url in service_discovery_urls:
        response = requests.get(discovery_url)
        config = response.json()
        filename = f"{config['name']}_{config['version']}.json"
        if 400 <= response.status_code < 500:
            print(f"Error: {response.status_code} - {filename}")
            continue
        output_file_path = os.path.join(download_path, filename)
        print(f"Success: {output_file_path}")
        with open(output_file_path, 'w') as output_file:
            json.dump(config, output_file, indent=2)


def gen_retry_predicate(
    err_codes: list[int],
    err_tags: list[str],
) -> dict:
    return {
        "params": ["e"],
        "steps": [
            {

                "assign": {
                    "assign": [
                        {"err_codes": err_codes},
                        {"err_tags": err_tags}
                    ]
                }
            },
            {
                "comment": {
                    "call": "sys.log",
                    "args": {
                        "text": "Running default predicate for err_codes: ${"
                                "string(err_codes)} and err_tags: ${string("
                                "err_tags)}",
                        "severity": "DEBUG"
                    }
                }
            },
            {
                "check_not_ok": {
                    "switch": [
                        {
                            # @formatter:off
                            "condition": "${e.code in err_codes or len(set(err_tags) & set(e.tags)) > 0}",
                            "return": True
                        }
                    ]
                }
            },
            {
                "log_error_not_handled": {
                    "call": "sys.log",
                    "args": {
                        "text": "Error not handled: ${e.tags[0]}: (${e.code}) ${e.message}",
                        "severity": "ERROR"
                    }
                }
            },
            {
                "raise_error": {
                    "return": False
                }
            }
        ]
    }


StepConfig: TypeAlias = dict[str, any]
Context: TypeAlias = dict[str, any]
NextStep: TypeAlias = Optional[str]
ReturnValue: TypeAlias = any

def load_package_config(config_path: str) -> dict:
    """Load a configuration file from a given path inside the package."""
    package_path = importlib.resources.files(__package__)
    file_path = package_path / config_path
    with file_path.open() as file:
        return yaml.safe_load(file)
