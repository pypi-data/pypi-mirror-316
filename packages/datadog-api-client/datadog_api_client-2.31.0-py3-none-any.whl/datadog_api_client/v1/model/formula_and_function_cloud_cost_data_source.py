# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class FormulaAndFunctionCloudCostDataSource(ModelSimple):
    """
    Data source for Cloud Cost queries.

    :param value: If omitted defaults to "cloud_cost". Must be one of ["cloud_cost"].
    :type value: str
    """

    allowed_values = {
        "cloud_cost",
    }
    CLOUD_COST: ClassVar["FormulaAndFunctionCloudCostDataSource"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


FormulaAndFunctionCloudCostDataSource.CLOUD_COST = FormulaAndFunctionCloudCostDataSource("cloud_cost")
