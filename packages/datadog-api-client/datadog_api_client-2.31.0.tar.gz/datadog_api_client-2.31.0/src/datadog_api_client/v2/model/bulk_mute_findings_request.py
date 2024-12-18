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
    from datadog_api_client.v2.model.bulk_mute_findings_request_data import BulkMuteFindingsRequestData


class BulkMuteFindingsRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.bulk_mute_findings_request_data import BulkMuteFindingsRequestData

        return {
            "data": (BulkMuteFindingsRequestData,),
        }

    attribute_map = {
        "data": "data",
    }

    def __init__(self_, data: BulkMuteFindingsRequestData, **kwargs):
        """
        The new bulk mute finding request.

        :param data: Data object containing the new bulk mute properties of the finding.
        :type data: BulkMuteFindingsRequestData
        """
        super().__init__(kwargs)

        self_.data = data
