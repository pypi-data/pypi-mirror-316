# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class DashboardType(ModelSimple):
    """
    The type of the dashboard.

    :param value: Must be one of ["custom_timeboard", "custom_screenboard", "integration_screenboard", "integration_timeboard", "host_timeboard"].
    :type value: str
    """

    allowed_values = {
        "custom_timeboard",
        "custom_screenboard",
        "integration_screenboard",
        "integration_timeboard",
        "host_timeboard",
    }
    CUSTOM_TIMEBOARD: ClassVar["DashboardType"]
    CUSTOM_SCREENBOARD: ClassVar["DashboardType"]
    INTEGRATION_SCREENBOARD: ClassVar["DashboardType"]
    INTEGRATION_TIMEBOARD: ClassVar["DashboardType"]
    HOST_TIMEBOARD: ClassVar["DashboardType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


DashboardType.CUSTOM_TIMEBOARD = DashboardType("custom_timeboard")
DashboardType.CUSTOM_SCREENBOARD = DashboardType("custom_screenboard")
DashboardType.INTEGRATION_SCREENBOARD = DashboardType("integration_screenboard")
DashboardType.INTEGRATION_TIMEBOARD = DashboardType("integration_timeboard")
DashboardType.HOST_TIMEBOARD = DashboardType("host_timeboard")
