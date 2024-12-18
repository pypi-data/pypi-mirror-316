# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class MetricDashboardType(ModelSimple):
    """
    Dashboard resource type.

    :param value: If omitted defaults to "dashboards". Must be one of ["dashboards"].
    :type value: str
    """

    allowed_values = {
        "dashboards",
    }
    DASHBOARDS: ClassVar["MetricDashboardType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


MetricDashboardType.DASHBOARDS = MetricDashboardType("dashboards")
