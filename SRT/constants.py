STATION_CODE = {
    "수서": "0551",
    "동탄": "0552",
    "평택지제": "0553",
    "곡성": "0049",
    "공주": "0514",
    "광주송정": "0036",
    "구례구": "0050",
    "김천(구미)": "0507",
    "나주": "0037",
    "남원": "0048",
    "대전": "0010",
    "동대구": "0015",
    "마산": "0059",
    "목포": "0041",
    "밀양": "0017",
    "부산": "0020",
    "서대구": "0506",
    "순천": "0051",
    "신경주": "0508",  # for backward compatibility
    "경주": "0508",
    "여수EXPO": "0053",
    "여천": "0139",
    "오송": "0297",
    "울산(통도사)": "0509",
    "익산": "0030",
    "전주": "0045",
    "정읍": "0033",
    "진영": "0056",
    "진주": "0063",
    "창원": "0057",
    "창원중앙": "0512",
    "천안아산": "0502",
    "포항": "0515",
}

STATION_NAME = {v: k for (k, v) in STATION_CODE.items()}

TRAIN_NAME = {
    "00": "KTX",
    "02": "무궁화",
    "03": "통근열차",
    "04": "누리로",
    "05": "전체",
    "07": "KTX-산천",
    "08": "ITX-새마을",
    "09": "ITX-청춘",
    "10": "KTX-산천",
    "17": "SRT",
    "18": "ITX-마음",
}

WINDOW_SEAT = {None: "000", True: "012", False: "013"}

SRT_MOBILE = "https://app.srail.or.kr:443"
API_ENDPOINTS = {
    "main": f"{SRT_MOBILE}/main/main.do",
    "login": f"{SRT_MOBILE}/apb/selectListApb01080_n.do",
    "logout": f"{SRT_MOBILE}/login/loginOut.do",
    "search_schedule": f"{SRT_MOBILE}/ara/selectListAra10007_n.do",
    "reserve": f"{SRT_MOBILE}/arc/selectListArc05013_n.do",
    "tickets": f"{SRT_MOBILE}/atc/selectListAtc14016_n.do",
    "ticket_info": f"{SRT_MOBILE}/ard/selectListArd02017_n.do?",
    "cancel": f"{SRT_MOBILE}/ard/selectListArd02045_n.do",
    "standby_option": f"{SRT_MOBILE}/ata/selectListAta01135_n.do",
    "payment": f"{SRT_MOBILE}/ata/selectListAta09036_n.do",
}

USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0_1 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Mobile/15E148 SRT-APP-iOS V.2.0.18"
)

INVALID_NETFUNNEL_KEY = "NET000001"
