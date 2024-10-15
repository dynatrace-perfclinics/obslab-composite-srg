# GitHub Actions Pipeline Integration

## Background
By defining our Workflow to orchestrate all the SRGs that are defined, we can now integrate the execution of that workflow
whenever a commit is made to a repository.

An example script is defined in this folder.

## Configuration

This Python Project uses Pydantic's `BaseSettings` class in-order to tune the code for the relevant environments.
All configurable parameters can be seen in `./composite_srg_pipeline/config.py`

- `DT_TOKEN_URL`: The OAUTH2 URL used to request a bearer token. Default Dynatrace URL is `https://sso.dynatrace.com/sso/oauth2/token`.
- `DT_CLIENT_ID`: OAUTH2 Client ID.  See [Dynatrace Documentation for further details](https://docs.dynatrace.com/docs/manage/identity-access-management/access-tokens-and-oauth-clients/oauth-clients#create-an-oauth2-client).
- `DT_CLIENT_SECRET`: OAUTH2 Client Secret.  See [Dynatrace Documentation for further details](https://docs.dynatrace.com/docs/manage/identity-access-management/access-tokens-and-oauth-clients/oauth-clients#create-an-oauth2-client).
- `DT_SRG_WORKFLOW_UUID`: Dynatrace has a workflow used to orchestrate execution of all prerequisite SRGs. This should be set to the UUID of that workflow.
- `DT_TASK_NAME`: In the above Composite SRG Workflow, there is a single step which is responsible for executing the Composite SRG. This field should correpsond to that name.
- `DT_TENANT_ID`: The 8 character Tenant ID taken from `https://<TENANT_ID>.apps.dynatrace.com/ui`
- `WORKFLOW_RETRY_COUNT` _[Optional]_: (3) | The number of attempts we will make to request the status of the Composite SRG Workflow before considering the execution a failure.
- `WORKFLOW_RETRY_DELAY` _[Optional]_: (50) | The time delay (in seconds) between retried API queries for Workflow status.
- `WORKFLOW_RETRY_MAX_DELAY` _[Optional]_: (150) | The longest period of time we will await for a non 'RUNNING' Workflow Status result
