# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    none_type,
    unset,
    UnsetType,
)


class TeamsResponseLinks(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "first": (str,),
            "last": (str, none_type),
            "next": (str,),
            "prev": (str, none_type),
            "self": (str,),
        }

    attribute_map = {
        "first": "first",
        "last": "last",
        "next": "next",
        "prev": "prev",
        "self": "self",
    }

    def __init__(
        self_,
        first: Union[str, UnsetType] = unset,
        last: Union[str, none_type, UnsetType] = unset,
        next: Union[str, UnsetType] = unset,
        prev: Union[str, none_type, UnsetType] = unset,
        self: Union[str, UnsetType] = unset,
        **kwargs,
    ):
        """
        Teams response links.

        :param first: First link.
        :type first: str, optional

        :param last: Last link.
        :type last: str, none_type, optional

        :param next: Next link.
        :type next: str, optional

        :param prev: Previous link.
        :type prev: str, none_type, optional

        :param self: Current link.
        :type self: str, optional
        """
        if first is not unset:
            kwargs["first"] = first
        if last is not unset:
            kwargs["last"] = last
        if next is not unset:
            kwargs["next"] = next
        if prev is not unset:
            kwargs["prev"] = prev
        if self is not unset:
            kwargs["self"] = self
        super().__init__(kwargs)
