# Unless explicitly stated otherwise all files in this repository are licensed under the Apache-2.0 License.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2019-Present Datadog, Inc.
from __future__ import annotations


from datadog_api_client.model_utils import (
    ModelComposed,
    cached_property,
)


class TableWidgetTextFormatReplace(ModelComposed):
    def __init__(self, **kwargs):
        """
        Replace rule for the table widget text format.

        :param type: Table widget text format replace all type.
        :type type: TableWidgetTextFormatReplaceAllType

        :param _with: Replace All type.
        :type _with: str

        :param substring: Text that will be replaced.
        :type substring: str
        """
        super().__init__(kwargs)

    @cached_property
    def _composed_schemas(_):
        # we need this here to make our import statements work
        # we must store _composed_schemas in here so the code is only run
        # when we invoke this method. If we kept this at the class
        # level we would get an error because the class level
        # code would be run when this module is imported, and these composed
        # classes don't exist yet because their module has not finished
        # loading
        from datadog_api_client.v1.model.table_widget_text_format_replace_all import TableWidgetTextFormatReplaceAll
        from datadog_api_client.v1.model.table_widget_text_format_replace_substring import (
            TableWidgetTextFormatReplaceSubstring,
        )

        return {
            "oneOf": [
                TableWidgetTextFormatReplaceAll,
                TableWidgetTextFormatReplaceSubstring,
            ],
        }
