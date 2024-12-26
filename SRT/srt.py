import json
import re
from datetime import datetime, timedelta

import requests  # type: ignore[import]

from . import constants
from .constants import INVALID_NETFUNNEL_KEY, STATION_CODE, USER_AGENT
from .errors import SRTError, SRTLoginError, SRTNotLoggedInError, SRTResponseError
from .netfunnel import NetFunnelHelper
from .passenger import Adult, Passenger
from .reservation import SRTReservation, SRTTicket
from .response_data import SRTResponseData
from .seat_type import SeatType
from .train import SRTTrain

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_NUMBER_REGEX = re.compile(r"(\d{3})-(\d{3,4})-(\d{4})")

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

RESULT_SUCCESS = "SUCC"
RESULT_FAIL = "FAIL"

RESERVE_JOBID = {
    "PERSONAL": "1101",  # 개인예약
    "STANDBY": "1102",  # 예약대기
}


class SRT:
    """SRT 클라이언트 클래스

    Args:
        srt_id (str): SRT 계정 아이디 (멤버십 번호, 이메일, 전화번호)
        srt_pw (str): SRT 계정 패스워드
        auto_login (bool): :func:`login` 함수 호출 여부
        verbose (bool): 디버깅용 로그 출력 여부
        netfunnel_helper (NetFunnelHelper, optional): netfunnel 키 를 관리합니다. 자세한 사항은 `advanced.md`의 '여러 SRT 간, netFunnelKey 공유하기'를 참고하세요

    >>> srt = SRT("1234567890", YOUR_PASSWORD) # with membership number
    >>> srt = SRT("def6488@gmail.com", YOUR_PASSWORD) # with email
    >>> srt = SRT("010-1234-xxxx", YOUR_PASSWORD) # with phone number
    """

    def __init__(
        self,
        srt_id: str,
        srt_pw: str,
        auto_login: bool = True,
        verbose: bool = False,
        netfunnel_helper: NetFunnelHelper | None = None,
    ) -> None:
        self._session = requests.session()
        self._session.headers.update(DEFAULT_HEADERS)
        self.netfunnel_helper = (
            netfunnel_helper if netfunnel_helper is not None else NetFunnelHelper()
        )

        self.srt_id: str = srt_id
        self.srt_pw: str = srt_pw
        self.verbose: bool = verbose

        self.is_login: bool = False

        if auto_login:
            self.login(srt_id, srt_pw)

    def _log(self, msg: str) -> None:
        if self.verbose:
            print("[*] " + msg)

    def login(self, srt_id: str | None = None, srt_pw: str | None = None):
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

        LOGIN_TYPES: dict[str, str] = {
            "MEMBERSHIP_ID": "1",
            "EMAIL": "2",
            "PHONE_NUMBER": "3",
        }

        if EMAIL_REGEX.match(srt_id):
            login_type = LOGIN_TYPES["EMAIL"]
        elif PHONE_NUMBER_REGEX.match(srt_id):
            login_type = LOGIN_TYPES["PHONE_NUMBER"]
            srt_id = re.sub("-", "", srt_id)  # hyphen is not sent
        else:
            login_type = LOGIN_TYPES["MEMBERSHIP_ID"]

        url = constants.API_ENDPOINTS["login"]
        data: dict[str, str] = {
            "auto": "Y",
            "check": "Y",
            "page": "menu",
            "deviceKey": "-",
            "customerYn": "",
            "login_referer": constants.API_ENDPOINTS["main"],
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

        if "Your IP Address Blocked due to abnormal access." in r.text:
            self.is_login = False
            raise SRTLoginError(r.text.strip())

        self.is_login = True
        self.membership_number = json.loads(r.text).get("userMap").get("MB_CRD_NO")

        return True

    def logout(self) -> bool:
        """SRT 서버에서 로그아웃합니다."""

        if not self.is_login:
            return True

        url = constants.API_ENDPOINTS["logout"]

        r = self._session.post(url=url)
        self._log(r.text)

        if not r.ok:
            raise SRTResponseError(r.text)

        self.is_login = False
        self.membership_number = None

        return True

    def search_train(
        self,
        dep: str,
        arr: str,
        date: str | None = None,
        time: str | None = None,
        time_limit: str | None = None,
        available_only: bool = True,
    ) -> list[SRTTrain]:
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

        trains = self._search_train(
            dep=dep,
            arr=arr,
            date=date,
            time=time,
            time_limit=time_limit,
            arr_code=arr_code,
            dep_code=dep_code,
            available_only=available_only,
            use_netfunnel_cache=True,
        )

        return trains

    def _search_train(
        self,
        dep: str,
        arr: str,
        date: str | None = None,
        time: str | None = None,
        time_limit: str | None = None,
        arr_code: str | None = None,
        dep_code: str | None = None,
        available_only: bool = True,
        use_netfunnel_cache: bool = True,
    ) -> list[SRTTrain]:
        """netfunnel_key를 발급받아 열차를 검색하는 내부 함수입니다.

        Args:
            dep (str): 출발역
            arr (str): 도착역
            date (str, optional): 출발 날짜 (yyyyMMdd) (default: 당일)
            time (str, optional): 출발 시각 (hhmmss) (default: 0시 0분 0초)
            time_limit (str, optional): 출발 시각 조회 한도 (hhmmss)
            arr_code (str, optional): 도착역 코드
            dep_code (str, optional): 출발역 코드
            available_only (bool, optional): 매진되지 않은 열차만 검색합니다 (default: True)
            use_netfunnel_cache (bool, optional): netfunnel 캐시 사용 여부, 사용하지 않으면 요청 시마다 새로 netfunnel 키를 요청합니다 (default: True)

        Returns:
            list[:class:`SRTTrain`]: 열차 리스트
        """

        netfunnelKey = self.netfunnel_helper.generate_netfunnel_key(use_netfunnel_cache)

        url = constants.API_ENDPOINTS["search_schedule"]
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
            "netfunnelKey": netfunnelKey,
        }

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            message_code = parser.message_code()
            if message_code == INVALID_NETFUNNEL_KEY and use_netfunnel_cache:
                self._log(f"Invalid netfunnel key: {netfunnelKey}, regenerating...")

                return self._search_train(
                    dep=dep,
                    arr=arr,
                    date=date,
                    time=time,
                    time_limit=time_limit,
                    arr_code=arr_code,
                    dep_code=dep_code,
                    available_only=available_only,
                    use_netfunnel_cache=False,
                )
            else:
                message = parser.message()
                raise SRTResponseError(message, message_code)

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

    def reserve(
        self,
        train: SRTTrain,
        passengers: list[Passenger] | None = None,
        special_seat: SeatType = SeatType.GENERAL_FIRST,
        window_seat: bool | None = None,
    ) -> SRTReservation:
        """열차를 예약합니다.

        >>> trains = srt.search_train("수서", "부산", "210101", "000000")
        >>> srt.reserve(trains[0])

        Args:
            train (:class:`SRTrain`): 예약할 열차
            passengers (list[:class:`Passenger`], optional): 예약 인원 (default: 어른 1명)
            special_seat (:class:`SeatType`): 일반실/특실 선택 유형 (default: 일반실 우선)
            window_seat (bool, optional): 창가 자리 우선 예약 여부

        Returns:
            :class:`SRTReservation`: 예약 내역
        """

        return self._reserve(
            RESERVE_JOBID["PERSONAL"],
            train,
            passengers,
            special_seat,
            window_seat=window_seat,
            use_netfunnel_cache=True,
        )

    def reserve_standby(
        self,
        train: SRTTrain,
        passengers: list[Passenger] | None = None,
        special_seat: SeatType = SeatType.GENERAL_FIRST,
        mblPhone: str | None = None,
    ) -> SRTReservation:
        """예약대기 신청 합니다.

        >>> trains = srt.search_train("수서", "부산", "210101", "000000")
        >>> srt.reserve_standby(trains[0])

        Args:
            train (:class:`SRTrain`): 예약할 열차
            passengers (list[:class:`Passenger`], optional): 예약 인원 (default: 어른 1명)
            special_seat (:class:`SeatType`): 일반실/특실 선택 유형 (default: 일반실 우선)
            mblPhone (str, optional): 휴대폰 번호

        Returns:
            :class:`SRTReservation`: 예약 내역
        """

        return self._reserve(
            RESERVE_JOBID["STANDBY"], train, passengers, special_seat, mblPhone=mblPhone
        )

    def _reserve(
        self,
        jobid: str,
        train: SRTTrain,
        passengers: list[Passenger] | None = None,
        special_seat: SeatType = SeatType.GENERAL_FIRST,
        mblPhone: str | None = None,
        window_seat: bool | None = None,
        use_netfunnel_cache: bool = True,
    ) -> SRTReservation:
        """예약 신청 요청 공통 함수

        Args:
            train (:class:`SRTrain`): 예약할 열차
            passengers (list[:class:`Passenger`], optional): 예약 인원 (default: 어른 1명)
            special_seat (:class:`SeatType`): 일반실/특실 선택 유형 (default: 일반실 우선)
            mblPhone (str, optional): 휴대폰 번호 | jobid가 RESERVE_JOBID["STANDBY"]일 경우에만 사용
            window_seat (bool, optional): 창가 자리 우선 예약 여부 | jobid가 RESERVE_JOBID["PERSONAL"]일 경우에만 사용
            use_netfunnel_cache (bool, optional): netfunnel 캐시 사용 여부, 사용하지 않으면 요청 시마다 새로 netfunnel 키를 요청합니다 (default: True)

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

        # 일반식 / 특실 좌석 선택 옵션에 따라 결정.
        is_special_seat = None
        if special_seat == SeatType.GENERAL_ONLY:  # 일반실만
            is_special_seat = False
        elif special_seat == SeatType.SPECIAL_ONLY:  # 특실만
            is_special_seat = True
        elif special_seat == SeatType.GENERAL_FIRST:  # 일반실 우선
            if train.general_seat_available():
                is_special_seat = False
            else:
                is_special_seat = True
        elif special_seat == SeatType.SPECIAL_FIRST:  # 특실 우선
            if train.special_seat_available():
                is_special_seat = True
            else:
                is_special_seat = False

        netfunnelKey = self.netfunnel_helper.generate_netfunnel_key(use_netfunnel_cache)

        url = constants.API_ENDPOINTS["reserve"]
        data = {
            "jobId": jobid,
            "jrnyCnt": "1",
            "jrnyTpCd": "11",
            "jrnySqno1": "001",
            "stndFlg": "N",
            "trnGpCd1": "300",  # 열차그룹코드 (좌석선택은 SRT만 가능하기때문에 무조건 300을 셋팅한다)"
            "trnGpCd": "109",  # 열차그룹코드
            "grpDv": "0",  # 단체 구분 (1: 단체)
            "rtnDv": "0",  # 편도 구분 (0: 편도, 1: 왕복)
            "stlbTrnClsfCd1": train.train_code,  # 역무열차종별코드1 (열차 목록 값)
            "dptRsStnCd1": train.dep_station_code,  # 출발역코드1 (열차 목록 값)
            "dptRsStnCdNm1": train.dep_station_name,  # 출발역이름1 (열차 목록 값)
            "arvRsStnCd1": train.arr_station_code,  # 도착역코드1 (열차 목록 값)
            "arvRsStnCdNm1": train.arr_station_name,  # 도착역이름1 (열차 목록 값)
            "dptDt1": train.dep_date,  # 출발일자1 (열차 목록 값)
            "dptTm1": train.dep_time,  # 출발일자1 (열차 목록 값)
            "arvTm1": train.arr_time,  # 도착일자1 (열차 목록 값)
            "trnNo1": "%05d" % int(train.train_number),  # 열차번호1 (열차 목록 값)
            "runDt1": train.dep_date,  # 운행일자1 (열차 목록 값)
            "dptStnConsOrdr1": train.dep_station_constitution_order,  # 출발역구성순서1 (열차 목록 값)
            "arvStnConsOrdr1": train.arr_station_constitution_order,  # 도착역구성순서1 (열차 목록 값)
            "dptStnRunOrdr1": train.dep_station_run_order,  # 출발역운행순서1 (열차 목록 값)
            "arvStnRunOrdr1": train.arr_station_run_order,  # 도착역운행순서1 (열차 목록 값)
            "mblPhone": mblPhone,
            "netfunnelKey": netfunnelKey,
        }

        # jobid가 RESERVE_JOBID["PERSONAL"]일 경우, data에 reserveType 추가
        if jobid == RESERVE_JOBID["PERSONAL"]:
            data.update(
                {
                    "reserveType": "11",
                }
            )

        data.update(
            Passenger.get_passenger_dict(
                passengers, special_seat=is_special_seat, window_seat=window_seat
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
        raise SRTError("Ticket not found: check reservation status")

    def reserve_standby_option_settings(
        self,
        reservation: SRTReservation | int,
        isAgreeSMS: bool,
        isAgreeClassChange: bool,
        telNo: str | None = None,
    ) -> bool:
        """예약대기 옵션을 적용 합니다.

        >>> trains = srt.search_train("수서", "부산", "210101", "000000")
        >>> srt.reserve_standby(trains[0])
        >>> srt.reserve_standby_option_settings("1234567890", True, True, "010-1234-xxxx")

        Args:
            reservation (:class:`SRTReservation` or int): 예약 번호
            isAgreeSMS (bool): SMS 수신 동의 여부
            isAgreeClassChange (bool): 좌석등급 변경 동의 여부
            telNo (str, optional): 휴대폰 번호
        Returns:
            bool: 예약대기 옵션 적용 성공 여부
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        if isinstance(reservation, SRTReservation):
            reservation = reservation.reservation_number

        url = constants.API_ENDPOINTS["standby_option"]

        data = {
            "pnrNo": reservation,
            "psrmClChgFlg": "Y" if isAgreeClassChange else "N",
            "smsSndFlg": "Y" if isAgreeSMS else "N",
            "telNo": telNo if isAgreeSMS else "",
        }

        r = self._session.post(url=url, data=data)

        return r.status_code == 200

    def get_reservations(self, paid_only: bool = False) -> list[SRTReservation]:
        """전체 예약 정보를 얻습니다.

        Args:
            paid_only (bool): 결제된 예약 내역만 가져올지 여부

        Returns:
            list[:class:`SRTReservation`]: 예약 리스트
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        url = constants.API_ENDPOINTS["tickets"]
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
            if (
                paid_only and pay["stlFlg"] == "N"
            ):  # paid_only가 참이면 결제된 예약내역만 보여줌
                continue
            ticket = self.ticket_info(train["pnrNo"])
            reservation = SRTReservation(train, pay, ticket)
            reservations.append(reservation)

        return reservations

    def ticket_info(self, reservation: SRTReservation | int) -> list[SRTTicket]:
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

        url = constants.API_ENDPOINTS["ticket_info"]
        data = {"pnrNo": reservation, "jrnySqno": "1"}

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        tickets = [SRTTicket(ticket) for ticket in parser.get_all()["trainListMap"]]

        return tickets

    def cancel(self, reservation: SRTReservation | int) -> bool:
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

        url = constants.API_ENDPOINTS["cancel"]
        data = {"pnrNo": reservation, "jrnyCnt": "1", "rsvChgTno": "0"}

        r = self._session.post(url=url, data=data)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        self._log(parser.message())

        return True

    def pay_with_card(
        self,
        reservation: SRTReservation,
        number: str,
        password: str,
        validation_number: str,
        expire_date: str,
        installment: int = 0,
        card_type: str = "J",
    ) -> bool:
        """결제합니다.

        >>> reservation = srt.reserve(train)
        >>> srt.pay_with_card(reservation, "1234567890123456", "12", "981204", "2309", 0, "J")

        Args:
            reservation (:class:`SRTReservation`): 예약 내역
            number (str): 결제신용카드번호 (하이픈(-) 제외)
            password (str): 카드비밀번호 앞 2자리
            validation_number (str): 생년월일 (card_type이 J인 경우) || 사업자번호 (card_type이 S인 경우)
            expire_date (str): 카드유효기간(YYMM)
            installment (int): 할부선택 (0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24)
            card_type (str): 카드타입 (J : 개인, S : 법인)

        Returns:
            bool: 결제 성공 여부
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        url = constants.API_ENDPOINTS["payment"]

        data = {
            "stlDmnDt": datetime.now().strftime("%Y%m%d"),  # 날짜 (yyyyMMdd)
            "mbCrdNo": self.membership_number,  # 회원번호
            "stlMnsSqno1": "1",  # 결제수단 일련번호1 (1고정값인듯)
            "ststlGridcnt": "1",  # 결제수단건수 (1고정값인듯)
            "totNewStlAmt": reservation.total_cost,  # 총 신규 결제금액
            "athnDvCd1": card_type,  # 카드타입 (J : 개인, S : 법인)
            "vanPwd1": password,  # 카드비밀번호 앞 2자리
            "crdVlidTrm1": expire_date,  # 카드유효기간(YYMM)
            "stlMnsCd1": "02",  # 결제수단코드1: (02:신용카드, 11:전자지갑, 12:포인트)
            "rsvChgTno": "0",  # 예약변경번호 (0 고정값인듯)
            "chgMcs": "0",  # 변경마이크로초 (0고정값인듯)
            "ismtMnthNum1": installment,  # 할부선택 (0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24)
            "ctlDvCd": "3102",  # 조정구분코드(3102 고정값인듯)
            "cgPsId": "korail",  # korail 고정
            "pnrNo": reservation.reservation_number,  # 예약번호
            "totPrnb": reservation.seat_count,  # 승차인원
            "mnsStlAmt1": reservation.total_cost,  # 결제금액1
            "crdInpWayCd1": "@",  # 카드입력방식코드 (@: 신용카드/ok포인트, "": 전자지갑)
            "athnVal1": validation_number,  # 생년월일/사업자번호
            "stlCrCrdNo1": number,  # 결제신용카드번호1
            "jrnyCnt": "1",  # 여정수(1 고정)
            "strJobId": "3102",  # 업무구분코드(3102 고정값인듯)
            "inrecmnsGridcnt": "1",  # 1 고정값인듯
            "dptTm": reservation.dep_time,  # 출발시간
            "arvTm": reservation.arr_time,  # 도착시간
            "dptStnConsOrdr2": "000000",  # 출발역구성순서2 (000000 고정)
            "arvStnConsOrdr2": "000000",  # 도착역구성순서2 (000000 고정)
            "trnGpCd": "300",  # 열차그룹코드(300 고정)
            "pageNo": "-",  # 페이지번호(- 고정)
            "rowCnt": "-",  # 한페이지당건수(- 고정)
            "pageUrl": "",  # 페이지URL (빈값 고정)
        }

        r = self._session.post(url=url, data=data)

        parser = json.loads(r.text)

        if (
            parser.get("outDataSets").get("dsOutput0")[0].get("strResult")
            == RESULT_FAIL
        ):
            raise SRTResponseError(
                parser.get("outDataSets").get("dsOutput0")[0].get("msgTxt")
            )

        return True
