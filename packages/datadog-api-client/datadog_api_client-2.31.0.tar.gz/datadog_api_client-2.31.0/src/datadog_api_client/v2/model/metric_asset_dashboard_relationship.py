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
    from datadog_api_client.v2.model.metric_dashboard_type import MetricDashboardType


class MetricAssetDashboardRelationship(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.metric_dashboard_type import MetricDashboardType

        return {
            "id": (str,),
            "type": (MetricDashboardType,),
        }

    attribute_map = {
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_, id: Union[str, UnsetType] = unset, type: Union[MetricDashboardType, UnsetType] = unset, **kwargs
    ):
        """
        An object of type ``dashboard`` that can be referenced in the ``included`` data.

        :param id: The related dashboard's ID.
        :type id: str, optional

        :param type: Dashboard resource type.
        :type type: MetricDashboardType, optional
        """
        if id is not unset:
            kwargs["id"] = id
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
