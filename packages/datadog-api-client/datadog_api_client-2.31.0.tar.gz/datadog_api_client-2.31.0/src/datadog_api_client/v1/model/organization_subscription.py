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


class OrganizationSubscription(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "type": (str,),
        }

    attribute_map = {
        "type": "type",
    }

    def __init__(self_, type: Union[str, UnsetType] = unset, **kwargs):
        """
        Subscription definition.

        :param type: The subscription type. Types available are ``trial`` , ``free`` , and ``pro``.
        :type type: str, optional
        """
        if type is not unset:
            kwargs["type"] = type
        super().__init__(kwargs)
