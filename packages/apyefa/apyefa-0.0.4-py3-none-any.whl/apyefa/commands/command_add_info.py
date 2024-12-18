import logging

from voluptuous import Any, Optional, Required, Schema

from apyefa.commands.command import Command

_LOGGER = logging.getLogger(__name__)


class CommandAdditionalInfo(Command):
    def __init__(self) -> None:
        super().__init__("XML_ADDINFO_REQUEST", "addinfo")

    def parse(self, data: dict):
        data = self._get_parser().parse(data)

        result = []

        return result

    def _get_params_schema(self) -> Schema:
        return Schema(
            {
                Required("outputFormat", default="rapidJSON"): Any("rapidJSON"),
                Required("coordOutputFormat", default="WGS84"): Any("WGS84"),
                Optional("filterDateValid"): str,
                Optional("filterDateValidDay"): str,
                Optional("filterDateValidMonth"): str,
                Optional("filterDateValidYear"): str,
                Optional("filterDateValidComponentsActive"): Any("0", "1", 0, 1),
                Optional("filterPublicationStatus"): Any("current", "history"),
                Optional("filterValidIntervalStart"): str,
                Optional("filterValidIntervalEnd"): str,
                Optional("filterOMC"): str,
                Optional("filterOMC_PlaceID"): str,
                Optional("filterLineNumberIntervalStart"): str,
                Optional("filterLineNumberIntervalEnd"): str,
                Optional("filterMOTType"): str,
                Optional("filterPNLineDir"): str,
                Optional("filterPNLineSub"): str,
                Optional("itdLPxx_selLine"): str,
                Optional("itdLPxx_selOperator"): str,
                Optional("itdLPxx_selStop"): str,
                Optional("line"): str,
                Optional("filterInfoID"): str,
                Optional("filterInfoType"): str,
                Optional("filterPriority"): str,
                Optional("filterProviderCode"): str,
                Optional("filterSourceSystemName"): str,
            }
        )
