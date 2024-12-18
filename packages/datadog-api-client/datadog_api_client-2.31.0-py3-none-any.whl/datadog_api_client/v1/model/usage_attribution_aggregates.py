# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)


class UsageAttributionAggregates(ModelSimple):
    """
    An array of available aggregates.


    :type value: [UsageAttributionAggregatesBody]
    """

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.usage_attribution_aggregates_body import UsageAttributionAggregatesBody

        return {
            "value": ([UsageAttributionAggregatesBody],),
        }
