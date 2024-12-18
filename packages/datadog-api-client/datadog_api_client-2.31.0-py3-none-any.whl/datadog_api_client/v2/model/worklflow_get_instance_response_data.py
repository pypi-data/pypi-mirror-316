# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v2.model.worklflow_get_instance_response_data_attributes import (
        WorklflowGetInstanceResponseDataAttributes,
    )


class WorklflowGetInstanceResponseData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.worklflow_get_instance_response_data_attributes import (
            WorklflowGetInstanceResponseDataAttributes,
        )

        return {
            "attributes": (WorklflowGetInstanceResponseDataAttributes,),
        }

    attribute_map = {
        "attributes": "attributes",
    }

    def __init__(self_, attributes: Union[WorklflowGetInstanceResponseDataAttributes, UnsetType] = unset, **kwargs):
        """
        The data of the instance response.

        :param attributes: The attributes of the instance response data.
        :type attributes: WorklflowGetInstanceResponseDataAttributes, optional
        """
        if attributes is not unset:
            kwargs["attributes"] = attributes
        super().__init__(kwargs)
