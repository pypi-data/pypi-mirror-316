# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datadog_api_client.model_utils import (
    ModelNormal,
    cached_property,
    unset,
    UnsetType,
)


if TYPE_CHECKING:
    from datadog_api_client.v1.model.list_stream_column import ListStreamColumn
    from datadog_api_client.v1.model.widget_formula import WidgetFormula
    from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
    from datadog_api_client.v1.model.formula_and_function_query_definition import FormulaAndFunctionQueryDefinition
    from datadog_api_client.v1.model.list_stream_query import ListStreamQuery
    from datadog_api_client.v1.model.formula_and_function_response_format import FormulaAndFunctionResponseFormat
    from datadog_api_client.v1.model.widget_sort_by import WidgetSortBy
    from datadog_api_client.v1.model.formula_and_function_metric_query_definition import (
        FormulaAndFunctionMetricQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_event_query_definition import (
        FormulaAndFunctionEventQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_process_query_definition import (
        FormulaAndFunctionProcessQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_apm_dependency_stats_query_definition import (
        FormulaAndFunctionApmDependencyStatsQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_apm_resource_stats_query_definition import (
        FormulaAndFunctionApmResourceStatsQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_slo_query_definition import (
        FormulaAndFunctionSLOQueryDefinition,
    )
    from datadog_api_client.v1.model.formula_and_function_cloud_cost_query_definition import (
        FormulaAndFunctionCloudCostQueryDefinition,
    )


class GeomapWidgetRequest(ModelNormal):
    @cached_property
    def openapi_types(_):
        from datadog_api_client.v1.model.list_stream_column import ListStreamColumn
        from datadog_api_client.v1.model.widget_formula import WidgetFormula
        from datadog_api_client.v1.model.log_query_definition import LogQueryDefinition
        from datadog_api_client.v1.model.formula_and_function_query_definition import FormulaAndFunctionQueryDefinition
        from datadog_api_client.v1.model.list_stream_query import ListStreamQuery
        from datadog_api_client.v1.model.formula_and_function_response_format import FormulaAndFunctionResponseFormat
        from datadog_api_client.v1.model.widget_sort_by import WidgetSortBy

        return {
            "columns": ([ListStreamColumn],),
            "formulas": ([WidgetFormula],),
            "log_query": (LogQueryDefinition,),
            "q": (str,),
            "queries": ([FormulaAndFunctionQueryDefinition],),
            "query": (ListStreamQuery,),
            "response_format": (FormulaAndFunctionResponseFormat,),
            "rum_query": (LogQueryDefinition,),
            "security_query": (LogQueryDefinition,),
            "sort": (WidgetSortBy,),
        }

    attribute_map = {
        "columns": "columns",
        "formulas": "formulas",
        "log_query": "log_query",
        "q": "q",
        "queries": "queries",
        "query": "query",
        "response_format": "response_format",
        "rum_query": "rum_query",
        "security_query": "security_query",
        "sort": "sort",
    }

    def __init__(
        self_,
        columns: Union[List[ListStreamColumn], UnsetType] = unset,
        formulas: Union[List[WidgetFormula], UnsetType] = unset,
        log_query: Union[LogQueryDefinition, UnsetType] = unset,
        q: Union[str, UnsetType] = unset,
        queries: Union[
            List[
                Union[
                    FormulaAndFunctionQueryDefinition,
                    FormulaAndFunctionMetricQueryDefinition,
                    FormulaAndFunctionEventQueryDefinition,
                    FormulaAndFunctionProcessQueryDefinition,
                    FormulaAndFunctionApmDependencyStatsQueryDefinition,
                    FormulaAndFunctionApmResourceStatsQueryDefinition,
                    FormulaAndFunctionSLOQueryDefinition,
                    FormulaAndFunctionCloudCostQueryDefinition,
                ]
            ],
            UnsetType,
        ] = unset,
        query: Union[ListStreamQuery, UnsetType] = unset,
        response_format: Union[FormulaAndFunctionResponseFormat, UnsetType] = unset,
        rum_query: Union[LogQueryDefinition, UnsetType] = unset,
        security_query: Union[LogQueryDefinition, UnsetType] = unset,
        sort: Union[WidgetSortBy, UnsetType] = unset,
        **kwargs,
    ):
        """
        An updated geomap widget.

        :param columns: Widget columns.
        :type columns: [ListStreamColumn], optional

        :param formulas: List of formulas that operate on queries.
        :type formulas: [WidgetFormula], optional

        :param log_query: The log query.
        :type log_query: LogQueryDefinition, optional

        :param q: The widget metrics query.
        :type q: str, optional

        :param queries: List of queries that can be returned directly or used in formulas.
        :type queries: [FormulaAndFunctionQueryDefinition], optional

        :param query: Updated list stream widget.
        :type query: ListStreamQuery, optional

        :param response_format: Timeseries, scalar, or event list response. Event list response formats are supported by Geomap widgets.
        :type response_format: FormulaAndFunctionResponseFormat, optional

        :param rum_query: The log query.
        :type rum_query: LogQueryDefinition, optional

        :param security_query: The log query.
        :type security_query: LogQueryDefinition, optional

        :param sort: The controls for sorting the widget.
        :type sort: WidgetSortBy, optional
        """
        if columns is not unset:
            kwargs["columns"] = columns
        if formulas is not unset:
            kwargs["formulas"] = formulas
        if log_query is not unset:
            kwargs["log_query"] = log_query
        if q is not unset:
            kwargs["q"] = q
        if queries is not unset:
            kwargs["queries"] = queries
        if query is not unset:
            kwargs["query"] = query
        if response_format is not unset:
            kwargs["response_format"] = response_format
        if rum_query is not unset:
            kwargs["rum_query"] = rum_query
        if security_query is not unset:
            kwargs["security_query"] = security_query
        if sort is not unset:
            kwargs["sort"] = sort
        super().__init__(kwargs)
