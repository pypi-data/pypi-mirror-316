# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.notebook_cell_response_attributes import NotebookCellResponseAttributes
    from datadog_api_client.v1.model.notebook_cell_resource_type import NotebookCellResourceType
    from datadog_api_client.v1.model.notebook_markdown_cell_attributes import NotebookMarkdownCellAttributes
    from datadog_api_client.v1.model.notebook_timeseries_cell_attributes import NotebookTimeseriesCellAttributes
    from datadog_api_client.v1.model.notebook_toplist_cell_attributes import NotebookToplistCellAttributes
    from datadog_api_client.v1.model.notebook_heat_map_cell_attributes import NotebookHeatMapCellAttributes
    from datadog_api_client.v1.model.notebook_distribution_cell_attributes import NotebookDistributionCellAttributes
    from datadog_api_client.v1.model.notebook_log_stream_cell_attributes import NotebookLogStreamCellAttributes


class NotebookCellResponse(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.notebook_cell_response_attributes import NotebookCellResponseAttributes
        from datadog_api_client.v1.model.notebook_cell_resource_type import NotebookCellResourceType

        return {
            "attributes": (NotebookCellResponseAttributes,),
            "id": (str,),
            "type": (NotebookCellResourceType,),
        }

    attribute_map = {
        "attributes": "attributes",
        "id": "id",
        "type": "type",
    }

    def __init__(
        self_,
        attributes: Union[
            NotebookCellResponseAttributes,
            NotebookMarkdownCellAttributes,
            NotebookTimeseriesCellAttributes,
            NotebookToplistCellAttributes,
            NotebookHeatMapCellAttributes,
            NotebookDistributionCellAttributes,
            NotebookLogStreamCellAttributes,
        ],
        id: str,
        type: NotebookCellResourceType,
        **kwargs,
    ):
        """
        The description of a notebook cell response.

        :param attributes: The attributes of a notebook cell response. Valid cell types are ``markdown`` , ``timeseries`` , ``toplist`` , ``heatmap`` , ``distribution`` ,
            ``log_stream``. `More information on each graph visualization type. <https://docs.datadoghq.com/dashboards/widgets/>`_
        :type attributes: NotebookCellResponseAttributes

        :param id: Notebook cell ID.
        :type id: str

        :param type: Type of the Notebook Cell resource.
        :type type: NotebookCellResourceType
        """
        super().__init__(kwargs)

        self_.attributes = attributes
        self_.id = id
        self_.type = type
