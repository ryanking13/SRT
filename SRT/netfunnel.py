import time

import requests

from .constants import SRT_MOBILE, USER_AGENT
from .errors import SRTNetFunnelError


class NetFunnelHelper:
    NETFUNNEL_URL = "http://nf.letskorail.com/ts.wseq"

    OP_CODE = {
        "getTidchkEnter": "5101",
        "chkEnter": "5002",
        "setComplete": "5004",
    }

    WAIT_STATUS_PASS = "200"  # No need to wait
    WAIT_STATUS_FAIL = "201"  # Need to wait
    ALREADY_COMPLETED = "502"  # already completed(set-complete)

    DEFAULT_HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": SRT_MOBILE,
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
    }

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self._cached_key = None

    def generate_netfunnel_key(self, use_cache: bool):
        key = self._get_netfunnel_key(use_cache)
        self._set_complete(key)
        return key

    def _get_netfunnel_key(self, use_cache: bool):
        """
        NetFunnel 키를 요청합니다.

        Args:
            use_cache (bool): 캐시 사용 여부, 캐시 사용 시 이전 요청에서 반환한 키를 반환합니다.

        Returns:
            str: NetFunnel 키
        """

        if use_cache and self._cached_key is not None:
            return self._cached_key

        params = {
            "opcode": self.OP_CODE["getTidchkEnter"],
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={self.OP_CODE['getTidchkEnter']};",
            "sid": "service_1",
            "aid": "act_10",
            "js": "true",
            self._get_timestamp_for_netfunnel(): "",
        }

        try:
            resp = self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            )
        except Exception as e:
            raise SRTNetFunnelError(e) from e

        netfunnel_resp = NetFunnelResponse.parse(resp.text)

        netfunnel_key = netfunnel_resp.get("key")
        if netfunnel_key is None:
            raise SRTNetFunnelError("NetFunnel key not found in response")

        if netfunnel_resp.get("status") == self.WAIT_STATUS_FAIL:
            # TODO: better logging
            print("접속자가 많아 대기열에 들어갑니다.")

            nwait = netfunnel_resp.get("nwait") or "<unknown>"

            netfunnel_key = self._wait_until_complete(netfunnel_key, nwait)

        self._cached_key = netfunnel_key

        return netfunnel_key

    def _wait_until_complete(self, key: str, nwait: str) -> str:
        """
        NetFunnel이 완료될 때까지 대기합니다.
        """

        params = {
            "opcode": self.OP_CODE["chkEnter"],
            "key": key,
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={self.OP_CODE['chkEnter']};",
            "ttl": 1,
            "sid": "service_1",
            "aid": "act_10",
            "js": "true",
            self._get_timestamp_for_netfunnel(): "",
        }

        try:
            resp = self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            )
        except Exception as e:
            raise SRTNetFunnelError(e) from e

        netfunnel_resp = NetFunnelResponse.parse(resp.text)

        nwait_ = netfunnel_resp.get("nwait")
        key_ = netfunnel_resp.get("key")
        if key_ is None:
            raise SRTNetFunnelError("NetFunnel key not found in response")

        if nwait_ and nwait_ != "0":
            print(f"대기인원: {nwait_}명")

            # 1 sec
            # TODO: find how to calculate the re-try interval
            time.sleep(1)

            return self._wait_until_complete(key_, nwait_)
        else:
            return key_

    def _set_complete(self, key: str):
        """
        NetFunnel 완료 요청을 보냅니다.

        Args:
            key (str): NetFunnel 키
        """

        params = {
            "opcode": self.OP_CODE["setComplete"],
            "key": key,
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={self.OP_CODE['setComplete']};",
            "js": "true",
            self._get_timestamp_for_netfunnel(): "",
        }

        try:
            resp = self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            )

        except Exception as e:
            raise SRTNetFunnelError(e) from e

        netfunnel_resp = NetFunnelResponse.parse(resp.text)
        if netfunnel_resp.get("status") not in [
            self.WAIT_STATUS_PASS,
            self.ALREADY_COMPLETED,
        ]:
            raise SRTNetFunnelError(f"Failed to complete NetFunnel: {netfunnel_resp}")

    def _get_timestamp_for_netfunnel(self):
        return int(time.time() * 1000)


class NetFunnelResponse:
    """
    Represents a NetFunnel response.
    """

    OP_CODE_KEY = "NetFunnel.gRtype"
    RESULT_KEY = "NetFunnel.gControl.result"

    RESULT_SUBKEYS = [
        "key",
        "nwait",
        "nnext",
        "tps",
        "ttl",
        "ip",
        "port",
        "msg",
    ]

    def __init__(self, response: str, data: dict[str, str]):
        self.response = response
        self.data = data

    @classmethod
    def parse(cls, response: str) -> "NetFunnelResponse":
        """
        The factory method to create a NetFunnelResponse object from a response string.

        the response string will be in the format of:

        ```
        NetFunnel.gRtype=5101;
        NetFunnel.gControl.result='5002:201:key=<key>&nwait=3&nnext=1&tps=11.247706&ttl=1&ip=<ip>&port=80';
        NetFunnel.gControl._showResult();
        ```
        """

        top_level_keys = [r.strip() for r in response.split(";")]

        data: dict[str, str] = {}
        for top_level_key in top_level_keys:

            if top_level_key.startswith(cls.OP_CODE_KEY):
                data["opcode"] = top_level_key[len(cls.OP_CODE_KEY) + 1 :]

            if top_level_key.startswith(cls.RESULT_KEY):
                results = top_level_key[len(cls.RESULT_KEY) + 1 :].strip("'").split(":")

                if len(results) != 3:
                    raise SRTNetFunnelError(
                        f"Invalid NetFunnel response format: {response}"
                    )

                code, status, result = results
                data["next_code"] = code  # dunno what this is...
                data["status"] = status

                result_keys = result.split("&")
                for key in result_keys:
                    for subkey in cls.RESULT_SUBKEYS:
                        if key.startswith(subkey):
                            data[subkey] = key.split("=")[1]
                            break

        return cls(response, data)

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def __str__(self):
        return self.response
