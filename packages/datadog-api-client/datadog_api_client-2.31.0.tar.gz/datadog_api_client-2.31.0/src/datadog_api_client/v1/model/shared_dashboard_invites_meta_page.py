# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


class SharedDashboardInvitesMetaPage(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "total_count": (int,),
        }

    attribute_map = {
        "total_count": "total_count",
    }

    def __init__(self_, total_count: Union[int, UnsetType] = unset, **kwargs):
        """
        Object containing the total count of invitations across all pages

        :param total_count: The total number of invitations on this shared board, across all pages.
        :type total_count: int, optional
        """
        if total_count is not unset:
            kwargs["total_count"] = total_count
        super().__init__(kwargs)
