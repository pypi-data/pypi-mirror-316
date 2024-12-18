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
    from datadog_api_client.v2.model.spans_aggregation_function import SpansAggregationFunction
    from datadog_api_client.v2.model.spans_compute_type import SpansComputeType


class SpansCompute(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.spans_aggregation_function import SpansAggregationFunction
        from datadog_api_client.v2.model.spans_compute_type import SpansComputeType

        return {
            "aggregation": (SpansAggregationFunction,),
            "interval": (str,),
            "metric": (str,),
            "type": (SpansComputeType,),
        }

    attribute_map = {
        "aggregation": "aggregation",
        "interval": "interval",
        "metric": "metric",
        "type": "type",
    }

    def __init__(
        self_,
        aggregation: SpansAggregationFunction,
        interval: Union[str, UnsetType] = unset,
        metric: Union[str, UnsetType] = unset,
        type: Union[SpansComputeType, UnsetType] = unset,
        **kwargs,
    ):
        """
        A compute rule to compute metrics or timeseries.

        :param aggregation: An aggregation function.
        :type aggregation: SpansAggregationFunction

        :param interval: The time buckets' size (only used for type=timeseries)
            Defaults to a resolution of 150 points.
        :type interval: str, optional

        :param metric: The metric to use.
        :type metric: str, optional

        :param type: The type of compute.
        :type type: SpansComputeType, optional
        """
        if interval is not unset:
            kwargs["interval"] = interval
        if metric is not unset:
            kwargs["metric"] = metric
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)

        self_.aggregation = aggregation
