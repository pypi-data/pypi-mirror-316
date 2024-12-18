"""
Edit an application key owned by current user returns "OK" response
"""

from os import environ
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.key_management_api import KeyManagementApi
from datadog_api_client.v2.model.application_key_update_attributes import ApplicationKeyUpdateAttributes
from datadog_api_client.v2.model.application_key_update_data import ApplicationKeyUpdateData
from datadog_api_client.v2.model.application_key_update_request import ApplicationKeyUpdateRequest
from datadog_api_client.v2.model.application_keys_type import ApplicationKeysType

# there is a valid "application_key" in the system
APPLICATION_KEY_DATA_ATTRIBUTES_NAME = environ["APPLICATION_KEY_DATA_ATTRIBUTES_NAME"]
APPLICATION_KEY_DATA_ID = environ["APPLICATION_KEY_DATA_ID"]

body = ApplicationKeyUpdateRequest(
    data=ApplicationKeyUpdateData(
        id=APPLICATION_KEY_DATA_ID,
        type=ApplicationKeysType.APPLICATION_KEYS,
        attributes=ApplicationKeyUpdateAttributes(
            name="Application Key for managing dashboards-updated",
        ),
    ),
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = KeyManagementApi(api_client)
    response = api_instance.update_current_user_application_key(app_key_id=APPLICATION_KEY_DATA_ID, body=body)

    print(response)
