# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Any, Dict, List, Union

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    date,
    datetime,
    none_type,
    unset,
    UnsetType,
    UUID,
)


class SecurityMonitoringSignalAttributes(ModelNormal):
    @cached_property
    def openapi_types(_):
        return {
            "custom": (
                {
                    str: (
                        bool,
                        date,
                        datetime,
                        dict,
                        float,
                        int,
                        list,
                        str,
                        UUID,
                        none_type,
                    )
                },
            ),
            "message": (str,),
            "tags": ([str],),
            "timestamp": (datetime,),
        }

    attribute_map = {
        "custom": "custom",
        "message": "message",
        "tags": "tags",
        "timestamp": "timestamp",
    }

    def __init__(
        self_,
        custom: Union[Dict[str, Any], UnsetType] = unset,
        message: Union[str, UnsetType] = unset,
        tags: Union[List[str], UnsetType] = unset,
        timestamp: Union[datetime, UnsetType] = unset,
        **kwargs,
    ):
        """
        The object containing all signal attributes and their
        associated values.

        :param custom: A JSON object of attributes in the security signal.
        :type custom: {str: (bool, date, datetime, dict, float, int, list, str, UUID, none_type,)}, optional

        :param message: The message in the security signal defined by the rule that generated the signal.
        :type message: str, optional

        :param tags: An array of tags associated with the security signal.
        :type tags: [str], optional

        :param timestamp: The timestamp of the security signal.
        :type timestamp: datetime, optional
        """
        if custom is not unset:
            kwargs["custom"] = custom
        if message is not unset:
            kwargs["message"] = message
        if tags is not unset:
            kwargs["tags"] = tags
        if timestamp is not unset:
            kwargs["timestamp"] = timestamp
        super().__init__(kwargs)
