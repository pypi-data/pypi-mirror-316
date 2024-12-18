# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.notebook_create_data_attributes import NotebookCreateDataAttributes
    from datadog_api_client.v1.model.notebook_resource_type import NotebookResourceType


class NotebookCreateData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebook_create_data_attributes import NotebookCreateDataAttributes
        from datadog_api_client.v1.model.notebook_resource_type import NotebookResourceType

        return {
            "attributes": (NotebookCreateDataAttributes,),
            "type": (NotebookResourceType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "type": "type",
    }

    def __init__(self_, attributes: NotebookCreateDataAttributes, type: NotebookResourceType, **kwargs):
        """
        The data for a notebook create request.

        :param attributes: The data attributes of a notebook.
        :type attributes: NotebookCreateDataAttributes

        :param type: Type of the Notebook resource.
        :type type: NotebookResourceType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.type = type
