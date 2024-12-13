import json

from .errors import SRTError, SRTResponseError


class SRTResponseData:
    """SRT Response data class
    parse JSON response from API request
    """

    STATUS_SUCCESS = "SUCC"
    STATUS_FAIL = "FAIL"

    def __init__(self, response):
        self._json = json.loads(response)
        self._status = {}

        # parse response data
        self._parse()

    def __str__(self):
        return self.dump()

    def dump(self):
        return json.dumps(self._json)

    def _parse(self):
        if "resultMap" in self._json:
            self._status = self._json["resultMap"][0]
            return

        if "ErrorCode" in self._json and "ErrorMsg" in self._json:
            raise SRTResponseError(
                f'Undefined result status "[{self._json["ErrorCode"]}]: {self._json["ErrorMsg"]}"'
            )
        raise SRTError(f"Unexpected case [{self._json}")

    def success(self):
        result = self._status.get("strResult", None)
        if result is None:
            raise SRTResponseError("Response status is not given")
        if result == self.STATUS_SUCCESS:
            return True
        elif result == self.STATUS_FAIL:
            return False
        else:
            raise SRTResponseError(f'Undefined result status "{result}"')

    def message(self):
        return self._status.get("msgTxt", "")

    def message_code(self):
        return self._status.get("msgCd", "")

    # get parse result
    def get_all(self):
        return self._json.copy()

    def get_status(self):
        return self._status.copy()
