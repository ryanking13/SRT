import time

import requests

from .constants import SRT_MOBILE, USER_AGENT
from .errors import SRTNetFunnelError


class NetFunnelHelper:
    NETFUNNEL_URL = "http://nf.letskorail.com/ts.wseq"

    OP_CODE = {
        "getTidchkEnter": "5101",
        "setComplete": "5004",
    }

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
        self._cachedNetfunnelKey = None

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

        if use_cache and self._cachedNetfunnelKey is not None:
            return self._cachedNetfunnelKey

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
            response = self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            ).text
        except Exception as e:
            raise SRTNetFunnelError(e) from e

        netfunnel_key = self._extract_netfunnel_key(response)
        self._cachedNetfunnelKey = netfunnel_key

        return netfunnel_key

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
            self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            )
        except Exception as e:
            raise SRTNetFunnelError(e) from e
        
    def _get_timestamp_for_netfunnel(self):
        return int(time.time() * 1000)

    def _extract_netfunnel_key(self, response: str):
        """
        NetFunnel 키를 추출합니다.

        Args:
            response (str): NetFunnel 응답

        Returns:
            str: NetFunnel 키

        Raises:
            SRTNetFunnelError: NetFunnel 키를 찾을 수 없는 경우
        """
        key_start = response.find("key=")
        if key_start == -1:
            raise SRTNetFunnelError("NetFunnel key not found in response")
            
        key_start += 4  # "key=" length
        key_end = response.find("&", key_start)
        if key_end == -1:
            raise SRTNetFunnelError("Invalid NetFunnel key format in response")
            
        return response[key_start:key_end]