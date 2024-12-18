# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.opsgenie_service_response_data import OpsgenieServiceResponseData


class OpsgenieServiceResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.opsgenie_service_response_data import OpsgenieServiceResponseData

        return {
            "data": (OpsgenieServiceResponseData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: OpsgenieServiceResponseData, **kwargs):
        """
        Response of an Opsgenie service.

        :param data: Opsgenie service data from a response.
        :type data: OpsgenieServiceResponseData
        """
        super().__init__(kwargs)

        self_.data = data
