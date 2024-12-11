import time

import requests

from .constants import SRT_MOBILE, USER_AGENT


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

    def get_netfunnel_key(self):
        timestamp = int(time.time() * 1000)
        response = self.session.get(
            self.NETFUNNEL_URL,
            params={
                "opcode": self.OP_CODE["getTidchkEnter"],
                "nfid": "0",
                "prefix": f"NetFunnel.gRtype={self.OP_CODE['getTidchkEnter']};",
                "sid": "service_1",
                "aid": "act_10",
                "js": "true",
                str(timestamp): "",
            },
        ).text

        key_start = response.find("key=") + 4
        key_end = response.find("&", key_start)
        return response[key_start:key_end]

    def set_complete(self, key: str):
        timestamp = int(time.time() * 1000)
        self.session.get(
            self.NETFUNNEL_URL,
            params={
                "opcode": self.OP_CODE["setComplete"],
                "key": key,
                "nfid": "0",
                "prefix": f"NetFunnel.gRtype={self.OP_CODE['setComplete']};",
                "js": "true",
                str(timestamp): "",
            },
        )
