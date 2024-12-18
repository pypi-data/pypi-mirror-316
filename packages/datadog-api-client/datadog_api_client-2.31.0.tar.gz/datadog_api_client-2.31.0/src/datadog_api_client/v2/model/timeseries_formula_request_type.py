# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class TimeseriesFormulaRequestType(ModelSimple):
    """
    The type of the resource. The value should always be timeseries_request.

    :param value: If omitted defaults to "timeseries_request". Must be one of ["timeseries_request"].
    :type value: str
    """

    allowed_values = {
        "timeseries_request",
    }
    TIMESERIES_REQUEST: ClassVar["TimeseriesFormulaRequestType"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


TimeseriesFormulaRequestType.TIMESERIES_REQUEST = TimeseriesFormulaRequestType("timeseries_request")
