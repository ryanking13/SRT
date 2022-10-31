import re
from datetime import datetime, timedelta

import requests  # type: ignore

from .constants import STATION_CODE
from .errors import SRTError, SRTLoginError, SRTNotLoggedInError, SRTResponseError
from .passenger import Adult, Passenger
from .reservation import SRTReservation, SRTTicket
from .response_data import SRTResponseData
from .train import SRTTrain

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_NUMBER_REGEX = re.compile(r"(\d{3})-(\d{3,4})-(\d{4})")

SCHEME = "https"
SRT_HOST = "app.srail.or.kr"
SRT_PORT = "443"

SRT_MOBILE = "{scheme}://{host}:{port}".format(
    scheme=SCHEME, host=SRT_HOST, port=SRT_PORT
)

SRT_MAIN = f"{SRT_MOBILE}/main/main.do"
SRT_LOGIN = f"{SRT_MOBILE}/apb/selectListApb01080_n.do"
SRT_LOGOUT = f"{SRT_MOBILE}/login/loginOut.do"
SRT_SEARCH_SCHEDULE = f"{SRT_MOBILE}/ara/selectListAra10007_n.do"
SRT_RESERVE = f"{SRT_MOBILE}/arc/selectListArc05013_n.do"
SRT_TICKETS = f"{SRT_MOBILE}/atc/selectListAtc14016_n.do"
SRT_TICKET_INFO = f"{SRT_MOBILE}/ard/selectListArd02017_n.do?"
SRT_CANCEL = f"{SRT_MOBILE}/ard/selectListArd02045_n.do"

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 5.1.1; LGM-V300K Build/N2G47H) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36SRT-APP-Android V.1.0.6"
    ),
    "Accept": "application/json",
}

RESULT_SUCCESS = "SUCC"
RESULT_FAIL = "FAIL"


class SRT:
    """SRT 클라이언트 클래스

    Args:
        srt_id (str): SRT 계정 아이디 (멤버십 번호, 이메일, 전화번호)
        srt_pw (str): SRT 계정 패스워드
        auto_login (bool): :func:`login` 함수 호출 여부
        verbose (bool): 디버깅용 로그 출력 여부

    >>> srt = SRT("1234567890", YOUR_PASSWORD) # with membership number
    >>> srt = SRT("def6488@gmail.com", YOUR_PASSWORD) # with email
    >>> srt = SRT("010-1234-xxxx", YOUR_PASSWORD) # with phone number
    """

    def __init__(self, srt_id, srt_pw, auto_login=True, verbose=False):
        self._session = requests.session()
        self._session.headers.update(DEFAULT_HEADERS)

        self.srt_id = srt_id
        self.srt_pw = srt_pw
        self.verbose = verbose

        self.is_login = False

        if auto_login:
            self.login(srt_id, srt_pw)

    def _log(self, msg):
        if self.verbose:
            print("[*] " + msg)

    def login(self, srt_id=None, srt_pw=None):
        """SRT 서버에 로그인합니다.

        일반적인 경우에는 인스턴스가 생성될 때에 자동으로 로그인 되므로,
        이 함수를 직접 호출할 필요가 없습니다.

        Args:
            srt_id (str, optional): SRT 계정 아이디
            srt_pwd (str, optional): SRT 계정 패스워드

        Returns:
            bool: 로그인 성공 여부
        """
        if srt_id is None:
            srt_id = self.srt_id
        else:
            self.srt_id = srt_id

        if srt_pw is None:
            srt_pw = self.srt_pw
        else:
            self.srt_pw = srt_pw

        LOGIN_TYPES = {"MEMBERSHIP_ID": "1", "EMAIL": "2", "PHONE_NUMBER": "3"}

        if EMAIL_REGEX.match(srt_id):
            login_type = LOGIN_TYPES["EMAIL"]
        elif PHONE_NUMBER_REGEX.match(srt_id):
            login_type = LOGIN_TYPES["PHONE_NUMBER"]
            srt_id = re.sub("-", "", srt_id)  # hyphen is not sent
        else:
            login_type = LOGIN_TYPES["MEMBERSHIP_ID"]

        url = SRT_LOGIN
        data = {
            "auto": "Y",
            "check": "Y",
            "page": "menu",
            "deviceKey": "-",
            "customerYn": "",
            "login_referer": SRT_MAIN,
            "srchDvCd": login_type,
            "srchDvNm": srt_id,
            "hmpgPwdCphd": srt_pw,
        }

        r = self._session.post(url=url, data=data)
        self._log(r.text)
        if "존재하지않는 회원입니다" in r.text:
            self.is_login = False
            raise SRTLoginError(r.json()["MSG"])

        if "비밀번호 오류" in r.text:
            self.is_login = False
            raise SRTLoginError(r.json()["MSG"])

        self.is_login = True
        return True
        # parser = SRTResponseData(r.text)

        # if parser.success():
        #     status, result, _, __ = parser.get_all()
        #     self.kr_session_id = status.get("KR_JSESSIONID")
        #     self.sr_session_id = status.get("SR_JSESSIONID")
        #     self.user_name = result.get("CUST_NM")
        #     self.user_membership_number = result.get("MB_CRD_NO")
        #     self.user_phone_number = result.get("MBL_PHONE")
        #     self.user_type = result.get("CUST_MG_SRT_NM")  # 개인고객 or ...
        #     self.user_level = result.get("CUST_DTL_SRT_NM")  # 일반회원 or ...
        #     self.user_sex = result.get("SEX_DV_NM")
        #     self._session.cookies.update({"gs_loginCrdNo": result.get("MB_CRD_NO")})

        #     self._log(parser.message())
        #     self.is_login = True
        #     return True

        # else:
        #     self.is_login = False
        #     raise SRTResponseError(parser.message())

    def logout(self):
        """SRT 서버에서 로그아웃합니다."""

        if not self.is_login:
            return

        url = SRT_LOGOUT

        r = self._session.post(url=url)

        if not r.ok:
            raise SRTResponseError(r.text)

        return True

    def search_train(
        self, dep, arr, date=None, time=None, time_limit=None, available_only=True
    ):
        """주어진 출발지에서 도착지로 향하는 SRT 열차를 검색합니다.

        Args:
            dep (str): 출발역
            arr (str): 도착역
            date (str, optional): 출발 날짜 (yyyyMMdd) (default: 당일)
            time (str, optional): 출발 시각 (hhmmss) (default: 0시 0분 0초)
            time_limit (str, optional): 출발 시각 조회 한도 (hhmmss)
            available_only (bool, optional): 매진되지 않은 열차만 검색합니다 (default: True)

        Returns:
            list[:class:`SRTTrain`]: 열차 리스트
        """

        if not self.is_login:
            raise SRTNotLoggedInError()

        if dep not in STATION_CODE:
            raise ValueError(f'Station "{dep}" not exists')
        if arr not in STATION_CODE:
            raise ValueError(f'Station "{arr}" not exists')

        dep_code = STATION_CODE[dep]
        arr_code = STATION_CODE[arr]

        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        if time is None:
            time = "000000"

        url = SRT_SEARCH_SCHEDULE
        data = {
            # course (1: 직통, 2: 환승, 3: 왕복)
            # TODO: support 환승, 왕복
            "chtnDvCd": "1",
            "arriveTime": "N",
            "seatAttCd": "015",
            # 검색 시에는 1명 기준으로 검색
            "psgNum": 1,
            "trnGpCd": 109,
            # train type (05: 전체, 17: SRT)
            "stlbTrnClsfCd": "05",
            # departure date
            "dptDt": date,
            # departure time
            "dptTm": time,
            # arrival station code
            "arvRsStnCd": arr_code,
            # departure station code
            "dptRsStnCd": dep_code,
        }

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        self._log(parser.message())
        all_trains = parser.get_all()["outDataSets"]["dsOutput1"]
        trains = [SRTTrain(train) for train in all_trains]

        # Note: updated api returns subarray of all trains,
        #       therefore, to retrieve all trains, retry unless there are no more trains
        while trains:
            last_dep_time = datetime.strptime(trains[-1].dep_time, "%H%M%S")
            next_dep_time = last_dep_time + timedelta(seconds=1)
            data["dptTm"] = next_dep_time.strftime("%H%M%S")
            r = self._session.post(url=url, data=data)
            parser = SRTResponseData(r.text)

            # When there is no more train, return code will be FAIL
            if not parser.success():
                break

            _all_trains = parser.get_all()["outDataSets"]["dsOutput1"]
            trains.extend([SRTTrain(train) for train in _all_trains])

        # Filter SRT only, drop KTX, ITX, ...
        trains = list(filter(lambda t: t.train_name == "SRT", trains))

        if available_only:
            trains = list(filter(lambda t: t.seat_available(), trains))

        if time_limit:
            trains = list(filter(lambda t: t.dep_time <= time_limit, trains))

        return trains

    def reserve(self, train, passengers=None, special_seat=False, window_seat=None):
        """열차를 예약합니다.

        >>> trains = srt.search_train("수서", "부산", "210101", "000000")
        >>> srt.reserve(trains[0])

        Args:
            train (:class:`SRTrain`): 예약할 열차
            passengers (list[:class:`Passenger`], optional): 예약 인원 (default: 어른 1명)
            special_seat (bool, optional): 특실 포함 여부
            window_seat (bool, optional): 창가 자리 우선 예약 여부

        Returns:
            :class:`SRTReservation`: 예약 내역
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        if not isinstance(train, SRTTrain):
            raise TypeError('"train" parameter must be a SRTTrain instance')

        if train.train_name != "SRT":
            raise ValueError(
                f'"SRT" expected for a train name, {train.train_name} given'
            )

        if passengers is None:
            passengers = [Adult()]
        passengers = Passenger.combine(passengers)

        url = SRT_RESERVE
        data = {
            "reserveType": "11",
            "jobId": "1101",  # 개인 예약
            "jrnyCnt": "1",
            "jrnyTpCd": "11",
            "jrnySqno1": "001",
            "stndFlg": "N",
            "trnGpCd1": "300",  # 열차그룹코드 (좌석선택은 SRT만 가능하기때문에 무조건 300을 셋팅한다)"
            "stlbTrnClsfCd1": train.train_code,
            "dptDt1": train.dep_date,
            "dptTm1": train.dep_time,
            "runDt1": train.dep_date,
            "trnNo1": "%05d" % int(train.train_number),
            "dptRsStnCd1": train.dep_station_code,
            "dptRsStnCdNm1": train.dep_station_name,
            "arvRsStnCd1": train.arr_station_code,
            "arvRsStnCdNm1": train.arr_station_name,
        }

        data.update(
            Passenger.get_passenger_dict(
                passengers, special_seat=special_seat, window_seat=window_seat
            )
        )

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        self._log(parser.message())
        reservation_result = parser.get_all()["reservListMap"][0]

        # find corresponding ticket and return it
        tickets = self.get_reservations()
        for ticket in tickets:
            if ticket.reservation_number == reservation_result["pnrNo"]:
                return ticket
        # if ticket not found, it's an error
        else:
            SRTError("Ticket not found: check reservation status")

    def get_reservations(self):
        """전체 예약 정보를 얻습니다.

        Returns:
            list[:class:`SRTReservation`]: 예약 리스트
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        url = SRT_TICKETS
        data = {"pageNo": "0"}

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        self._log(parser.message())

        train_data = parser.get_all()["trainListMap"]
        pay_data = parser.get_all()["payListMap"]
        reservations = []
        for train, pay in zip(train_data, pay_data):
            ticket = self.ticket_info(train["pnrNo"])
            reservation = SRTReservation(train, pay, ticket)
            reservations.append(reservation)

        return reservations

    def ticket_info(self, reservation):
        """예약에 포함된 티켓 정보를 반환합니다.

        >>> reservations = srt.get_reservations()
        >>> reservations
        # [[SRT] 09월 30일, 수서~부산(15:30~18:06) 130700원(3석), 구입기한 09월 19일 19:11]
        >>> reservations[0].tickets
        # [18호차 9C (일반실) 어른/청소년 [52300원(600원 할인)],
        # 18호차 10C (일반실) 어른/청소년 [52300원(600원 할인)],
        # 18호차 10D (일반실) 장애 4~6급 [26100원(26800원 할인)]]

        Args:
            reservation (:class:`SRTReservation` or int): 예약 번호

        Returns:
            list[:class:`SRTTicket`]
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        if isinstance(reservation, SRTReservation):
            reservation = reservation.reservation_number

        url = SRT_TICKET_INFO
        data = {"pnrNo": reservation, "jrnySqno": "1"}

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        tickets = [SRTTicket(ticket) for ticket in parser.get_all()["trainListMap"]]

        return tickets

    def cancel(self, reservation):
        """예약을 취소합니다.

        >>> reservation = srt.reserve(train)
        >>> srt.cancel(reservation)
        >>> reservations = srt.get_reservations()
        >>> srt.cancel(reservations[0])

        Args:
            reservation (:class:`SRTReservation` or int): 예약 번호

        Returns:
            bool: 예약 취소 성공 여부
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        if isinstance(reservation, SRTReservation):
            reservation = reservation.reservation_number

        url = SRT_CANCEL
        data = {"pnrNo": reservation, "jrnyCnt": "1", "rsvChgTno": "0"}

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        self._log(parser.message())

        return True
