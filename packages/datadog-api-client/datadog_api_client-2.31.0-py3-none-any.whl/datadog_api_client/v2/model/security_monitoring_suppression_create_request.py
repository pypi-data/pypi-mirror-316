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
    from datadog_api_client.v2.model.security_monitoring_suppression_create_data import (
        SecurityMonitoringSuppressionCreateData,
    )


class SecurityMonitoringSuppressionCreateRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.security_monitoring_suppression_create_data import (
            SecurityMonitoringSuppressionCreateData,
        )

        return {
            "data": (SecurityMonitoringSuppressionCreateData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: SecurityMonitoringSuppressionCreateData, **kwargs):
        """
        Request object that includes the suppression rule that you would like to create.

        :param data: Object for a single suppression rule.
        :type data: SecurityMonitoringSuppressionCreateData
        """
        super().__init__(kwargs)

        self_.data = data
