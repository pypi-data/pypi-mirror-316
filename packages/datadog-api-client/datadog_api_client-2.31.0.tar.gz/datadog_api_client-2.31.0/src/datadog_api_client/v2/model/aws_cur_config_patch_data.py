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
    from datadog_api_client.v2.model.aws_cur_config_patch_request_attributes import AwsCURConfigPatchRequestAttributes
    from datadog_api_client.v2.model.aws_cur_config_patch_request_type import AwsCURConfigPatchRequestType


class AwsCURConfigPatchData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.aws_cur_config_patch_request_attributes import (
            AwsCURConfigPatchRequestAttributes,
        )
        from datadog_api_client.v2.model.aws_cur_config_patch_request_type import AwsCURConfigPatchRequestType

        return {
            "attributes": (AwsCURConfigPatchRequestAttributes,),
            "type": (AwsCURConfigPatchRequestType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: AwsCURConfigPatchRequestAttributes, type: AwsCURConfigPatchRequestType, **kwargs):
        """
        AWS CUR config Patch data.

        :param attributes: Attributes for AWS CUR config Patch Request.
        :type attributes: AwsCURConfigPatchRequestAttributes

        :param type: Type of AWS CUR config Patch Request.
        :type type: AwsCURConfigPatchRequestType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
