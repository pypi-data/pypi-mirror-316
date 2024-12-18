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
    from datadog_api_client.v2.model.create_data_deletion_request_body_attributes import (
        CreateDataDeletionRequestBodyAttributes,
    )


class CreateDataDeletionRequestBodyData(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.create_data_deletion_request_body_attributes import (
            CreateDataDeletionRequestBodyAttributes,
        )

        return {
            "attributes": (CreateDataDeletionRequestBodyAttributes,),
        }

    attribute_map = {
        "attributes": "attributes",
    }

    def __init__(self_, attributes: CreateDataDeletionRequestBodyAttributes, **kwargs):
        """
        Data needed to create a data deletion request.

        :param attributes: Attributes for creating a data deletion request.
        :type attributes: CreateDataDeletionRequestBodyAttributes
        """
        super().__init__(kwargs)

        self_.attributes = attributes
