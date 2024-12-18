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
    from datadog_api_client.v2.model.service_now_ticket_result import ServiceNowTicketResult
    from datadog_api_client.v2.model.case3rd_party_ticket_status import Case3rdPartyTicketStatus


class ServiceNowTicket(ModelNormal):
    _nullable = True

    @cached_property
    def openapi_types(_):
        from datadog_api_client.v2.model.service_now_ticket_result import ServiceNowTicketResult
        from datadog_api_client.v2.model.case3rd_party_ticket_status import Case3rdPartyTicketStatus

        return {
            "result": (ServiceNowTicketResult,),
            "status": (Case3rdPartyTicketStatus,),
        }

    attribute_map = {
        "result": "result",
        "status": "status",
    }
    read_only_vars = {
        "status",
    }

    def __init__(
        self_,
        result: Union[ServiceNowTicketResult, UnsetType] = unset,
        status: Union[Case3rdPartyTicketStatus, UnsetType] = unset,
        **kwargs,
    ):
        """
        ServiceNow ticket attached to case

        :param result: ServiceNow ticket information
        :type result: ServiceNowTicketResult, optional

        :param status: Case status
        :type status: Case3rdPartyTicketStatus, optional
        """
        if result is not unset:
            kwargs["result"] = result
        if status is not unset:
            kwargs["status"] = status
        super().__init__(kwargs)
