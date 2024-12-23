# Google Cloud Workflows Emulator

This is both a library and cli tool.

## Using the CLI

### Calling a workflow

1. Create a workflow config for your project

   ```yaml
   # small_config.workflow.yaml
   main:
     params: [ table_name ]
     steps:
       - assign_variables:
           assign:
             - table_parts: ${text.split(table_name, ".")}
             - project_id: ${sys.get_env("GOOGLE_CLOUD_PROJECT_ID")}
             - dataset_id: ${table_parts[-2]}
             - table_id: ${table_parts[-1]}
             - config:
                 project_id: ${project_id}
                 dataset_id: ${dataset_id}
                 table_id: ${table_id}
             - query: |
                 SELECT column_name
                 FROM `${project_id}.${dataset_id}.INFORMATION_SCHEMA.COLUMNS`
                 WHERE table_name = '${table_id}'
       - final:
           return: ${query}
   ```

   
   | ⚠ NOTE                                                                                                                              |
   |-------------------------------------------------------------------------------------------------------------------------------------|
   | Rember to use the Cloud Workflows Json schema in your IDE to get the correct syntax highlighting, autocompletion and error checking. |
  

2. Define your environment variables in the `.env` file. Alternatively you can
   pass a custom `.env` file to the emulator with the `--env-file` flag.

   ```dotenv
   # .env
   GOOGLE_CLOUD_PROJECT_ID=numbers-crunching-123
   ```

3. To run a single workflow in the CLI:
   ```shell
   workflows-emulator \
     --config test/data/small_config.workflow.yaml \
     run \
     --data='{"var_content": "lowercase text"}'
   ```
   
   To start the server emulating the Google Cloud service:
   ```shell
   workflows-emulator --config test/data/small_config.workflow.yaml serve
   ```
   and then call the server with a POST request:
   ```shell
   curl --request 'POST' \
      --header 'Content-Type: application/json' \
      --data '{"argument": "{\"var_content\": \"hello\"}"}' \
      'http://localhost:8000/v1/projects/my_project/locations/europe-west4/workflows/small_config/executions'
   ```

4. The output will be printed to the console
    ```
    Log step HELLO
    "HELLO"
    ```

## Using the library for testing

Given this workflow
```yaml
main:
  params: [ my_var ]
  steps:
     - call_subworkflow:
          call: addition
          args:
             operand_a: ${my_var}
             operand_b: 2
          result: added
     - final:
          return: ${added}

addition:
  params: [ operand_a, operand_b ]
  steps:
    - log:
        call: sys.log
        args:
           text: ${"Adding " + string(operand_a) + " and " + string(operand_b)}
    - process:
        return: ${operand_a + operand_b}
```

You can write unit tests for it like so:
```python
import os
from workflows_emulator.main import (
   execute_step, load_workflow,
   execute_workflow, execute_subworkflow,
   get_step,
)

def test_load_workflow():
   """Fails if syntax is wrong"""
   load_workflow('path/to/workflow.yaml')

def test_main_workflow():
   """Checks wether it calculates correctly"""
   config = load_workflow('path/to/workflow.yaml')
   params = {'my_var': 3}
   result = execute_workflow(config, params)
   assert result == 5


def test_subworkflow():
   config = load_workflow('path/to/workflow.yaml')
   params = {'operand_a': 1, 'operand_b': 2}
   result = execute_subworkflow(config['addition'], params)
   assert result == 3


def test_step():
   config = load_workflow('path/to/workflow.yaml')
   subworkflow_step_list = config['addition']['steps']
   ok, _index, step_config = get_step(subworkflow_step_list, 'process')
   assert ok
   context = {'operand_a': 1, 'operand_b': 2}
   _context, _next, result = execute_step(step_config, context)
   assert result == 3
```

-----------

# Reason behind this emulator

## How to develop and debug your workflows according to Google Cloud

Running a Workflow goes like this:

```shell
WORKFLOW_NAME=my-workflow-name
WORKFLOW_FILE_PATH=my_workflow.yaml

gcloud workflows deploy ${WORKFLOW_NAME} \
  --location=europe-west4 \
  --call-log-level=log-all-calls \
  --source=${WORKFLOW_FILE_PATH}

gcloud workflows run ${WORKFLOW_NAME} \
  --location=europe-west4 \
  --call-log-level=log-all-calls
```

# Update connectors

Workflows provides a set of connectors to interact with Google Cloud REST APIs
easier. They are listed in the [documentation](https://cloud.google.com/workflows/docs/reference/googleapis).
If new connectors are added, they can be refreshed running:
```shell
get-discovery-documents
```

Then open a PR with the newly generated files.

# Not implemented (yet)

Some of the std lib modules are not implemented as the behavior is difficult
to mimic, or it is work-in-progress:

* experimental.executions — it's use is discouraged in the docs
* events — callbacks are complex to run locally
