# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelSimple,
    cached_property,
)

from typing import ClassVar


class CIAppPipelineEventStepStatus(ModelSimple):
    """
    The final status of the step.

    :param value: Must be one of ["success", "error"].
    :type value: str
    """

    allowed_values = {
        "success",
        "error",
    }
    SUCCESS: ClassVar["CIAppPipelineEventStepStatus"]
    ERROR: ClassVar["CIAppPipelineEventStepStatus"]

    @cached_property
    def openapi_types(_):
        return {
            "value": (str,),
        }


CIAppPipelineEventStepStatus.SUCCESS = CIAppPipelineEventStepStatus("success")
CIAppPipelineEventStepStatus.ERROR = CIAppPipelineEventStepStatus("error")
