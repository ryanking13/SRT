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

    def get_netfunnel_key(self, use_cache: bool):
        """
        NetFunnel 키를 요청합니다.

        Args:
            use_cache (bool): 캐시 사용 여부, 캐시 사용 시 이전 요청에서 반환한 키를 반환합니다.

        Returns:
            str: NetFunnel 키
        """
        
        if use_cache and self._cachedNetfunnelKey is not None:
            return self._cachedNetfunnelKey

        timestamp = int(time.time() * 1000)

        params = {
            "opcode": self.OP_CODE["getTidchkEnter"],
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={self.OP_CODE['getTidchkEnter']};",
            "sid": "service_1", 
            "aid": "act_10",
            "js": "true",
            str(timestamp): "",
        }

        try:
            response = self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            ).text

            key_start = response.find("key=") + 4
            key_end = response.find("&", key_start)
            netfunnel_key = response[key_start:key_end]
            self._cachedNetfunnelKey = netfunnel_key

            return netfunnel_key
        except Exception as e:
            raise SRTNetFunnelError(e)
    
    def set_complete(self, key: str):
        """
        NetFunnel 완료 요청을 보냅니다.

        Args:
            key (str): NetFunnel 키
        """
        timestamp = int(time.time() * 1000)

        params = {
            "opcode": self.OP_CODE["setComplete"],
            "key": key,
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={self.OP_CODE['setComplete']};",
            "js": "true",
            str(timestamp): "",
        }

        try:
            self.session.get(
                self.NETFUNNEL_URL,
                params=params,
            )
        except Exception as e:
            raise SRTNetFunnelError(e)

