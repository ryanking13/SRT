from datetime import datetime
import re
import requests
from .constants import STATION_CODE
from .errors import *
from .passenger import *
from .request_data import SRTRequestData
from .reservation import SRTReservation, SRTTicket
from .response_data import SRTResponseData
from .train import SRTTrain

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
PHONE_NUMBER_REGEX = re.compile(r'(\d{3})-(\d{3,4})-(\d{4})')

SCHEME = 'https'
SRT_HOST = 'app.srail.co.kr'
SRT_PORT = '443'

SRT_MOBILE = '{scheme}://{host}:{port}'.format(scheme=SCHEME, host=SRT_HOST, port=SRT_PORT)
SRT_LOGIN = '{}/apb/selectListApb01080.do'.format(SRT_MOBILE)
SRT_LOGOUT = '{}/apb/selectListApb01081.do'.format(SRT_MOBILE)
SRT_SEARCH_SCHEDULE = '{}/ara/selectListAra10007.do'.format(SRT_MOBILE)
SRT_RESERVE = '{}/arc/selectListArc05013.do'.format(SRT_MOBILE)
SRT_TICKETS = '{}/atc/selectListAtc14016.do'.format(SRT_MOBILE)
SRT_TICKET_INFO = '{}/ard/selectListArd02017.do'.format(SRT_MOBILE)
SRT_CANCEL = '{}/ard/selectListArd02045.do'.format(SRT_MOBILE)

STATUS_SUCCESS = 'SUCC'
STATUS_FAIL = 'FAIL'

DEFAULT_HEADERS = {
    'User-Agent': 'nexacroplatform14-android/2014 (compatible; Mozilla/4.0; MSIE 7.0)',
}

DEFAULT_COOKIES = {
    'gs_loginCrdNo': '0000000000',
}


class SRT:
    """SRT object"""

    def __init__(self, srt_id, srt_pw, auto_login=True, verbose=False):
        self._session = requests.session()
        self._session.headers.update(DEFAULT_HEADERS)
        self._session.cookies.update(DEFAULT_COOKIES)

        self.srt_id = srt_id
        self.srt_pw = srt_pw
        self.verbose = verbose

        self.is_login = False

        # xml column으로 제공해야하는 session id
        self.kr_session_id = ''
        self.sr_session_id = ''

        self.user_name = ''
        self.user_membership_number = ''
        self.user_phone_number = ''
        self.user_type = ''  # 개인고객 or ...
        self.user_level = ''  # 일반회원 or ...
        self.user_sex = ''

        if auto_login:
            self.login(srt_id, srt_pw)

    def _log(self, msg):
        if self.verbose:
            print('[*] ' + msg)

    def login(self, srt_id=None, srt_pw=None):

        if srt_id is None:
            srt_id = self.srt_id
        else:
            self.srt_id = srt_id

        if srt_pw is None:
            srt_pw = self.srt_pw
        else:
            self.srt_pw = srt_pw

        LOGIN_TYPES = {
            'MEMBERSHIP_ID': '1',
            'EMAIL': '2',
            'PHONE_NUMBER': '3',
        }

        if EMAIL_REGEX.match(srt_id):
            login_type = LOGIN_TYPES['EMAIL']
        elif PHONE_NUMBER_REGEX.match(srt_id):
            login_type = LOGIN_TYPES['PHONE_NUMBER']
            srt_id = re.sub('-', '', srt_id)  # hypen is not sent
        else:
            login_type = LOGIN_TYPES['MEMBERSHIP_ID']

        url = SRT_LOGIN
        data = SRTRequestData()
        data.update_datasets({
            'srchDvCd': login_type,
            'srchDvNm': srt_id,
            'hmpgPwdCphd': srt_pw,
        })

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)

        if parser.success():
            status, result, _, __ = parser.get_all()
            self.kr_session_id = status.get('KR_JSESSIONID')
            self.sr_session_id = status.get('SR_JSESSIONID')
            self.user_name = result.get('CUST_NM')
            self.user_membership_number = result.get('MB_CRD_NO')
            self.user_phone_number = result.get('MBL_PHONE')
            self.user_type = result.get('CUST_MG_SRT_NM')  # 개인고객 or ...
            self.user_level = result.get('CUST_DTL_SRT_NM')  # 일반회원 or ...
            self.user_sex = result.get('SEX_DV_NM')
            self._session.cookies.update({'gs_loginCrdNo': result.get('MB_CRD_NO')})

            self._log(parser.message())
            self.is_login = True
            return True

        else:
            self.is_login = False
            raise SRTResponseError(parser.message())

    def logout(self):
        if not self.is_login:
            return

        url = SRT_LOGOUT
        data = SRTRequestData()
        data.update_datasets({
            'KR_JSESSIONID': self.kr_session_id,
            'SR_JSESSIONID': self.sr_session_id,
        })

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)

        if parser.success():
            self._log(parser.message())
            self.is_login = False
            return True
        else:
            raise SRTResponseError(parser.message())

    def get_userinfo(self):
        if not self.is_login:
            return SRTNotLoggedInError()

        return {
            'name': self.user_name,
            'membership_number': self.user_membership_number,
            'phone_number': self.user_phone_number,
            'type': self.user_type,
            'level': self.user_level,
            'sex': self.user_sex,
        }

    def search_train(self, dep, arr, date=None, time=None, available_only=True):
        if not self.is_login:
            raise SRTNotLoggedInError()

        if dep not in STATION_CODE:
            raise ValueError('Station "{}" not exists'.format(dep))
        if arr not in STATION_CODE:
            raise ValueError('Station "{}" not exists'.format(arr))

        dep_code = STATION_CODE[dep]
        arr_code = STATION_CODE[arr]

        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        if time is None:
            time = datetime.now().strftime("%H%M%S")

        url = SRT_SEARCH_SCHEDULE
        data = SRTRequestData()
        data.update_datasets({
            # course (1: 직통, 2: 환승, 3: 왕복)
            # TODO: support 환승, 왕복
            'chtnDvCd': '1',
            # departure date
            'dptDt': date,
            # departure time
            'dptTm': time,
            # departure station code
            'dptRsStnCd': dep_code,
            # arrival station code
            'arvRsStnCd': arr_code,
            # train type (05: 전체, 17: SRT)
            'stlbTrnClsfCd': '17',
            # train group (109: 전체, 300: SRT, 900: SRT+KTX)
            'trnGpCd': '300',

            'psgNum': '1',
            'seatAttCd': '015',
            'arriveTime': 'N',
        })

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)
        data = parser.get_data1()

        if parser.success():
            self._log(parser.message())
            trains = []
            for d in data:
                trains.append(SRTTrain(d))

            if available_only:
                trains = list(filter(lambda t: t.seat_available(), trains))

            return trains
        else:
            raise SRTResponseError(parser.message())

    def reserve(self, train, passengers=None, special_seat=False):
        if not self.is_login:
            raise SRTNotLoggedInError()

        if not isinstance(train, SRTTrain):
            raise TypeError('"train" parameter must be SRTTrain instance')

        if train.train_name != 'SRT':
            raise ValueError('"SRT" expected for train name, {} given'.format(train.train_name))

        if passengers is None:
            passengers = [Adult()]
        passengers = Passenger.combine(passengers)

        url = SRT_RESERVE
        data = SRTRequestData()
        data.update_datasets({
            'dptDt1': train.dep_date,
            'dptTm1': train.dep_time,
            'runDt1': train.dep_date,
            'trnNo1': '%05d' % int(train.train_number),
            'dptRsStnCd1': train.dep_station_code,
            'dptRsStnCdNm1': train.dep_station_name,
            'arvRsStnCd1': train.arr_station_code,
            'arvRsStnCdNm1': train.arr_station_name,

            # seat location ('000': 기본, '012': 창측, '013': 복도측)
            # TODO: 선택 가능하게
            'locSeatAttCd1': '000',
            # seat requirement ('015': 일반, '021': 휠체어)
            # TODO: 선택 가능하게
            'rqSeatAttCd1': '015',

            # seat type: ('1': 일반실, '2': 특실)
            'psrmClCd1': '2' if special_seat else '1',

            'MB_CRD_NO': self.user_membership_number,
            'KR_JSESSIONID': self.kr_session_id,
            'SR_JSESSIONID': self.sr_session_id,
        })

        data.update_datasets(Passenger.get_passenger_dict(passengers))

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)
        data = parser.get_data1()

        if parser.success():
            self._log(parser.message())
            # find corresponding ticket and return it
            tickets = self.get_reservations()
            for ticket in tickets:
                if ticket.reservation_number == data[0]['pnrNo']:
                    return ticket
            # if ticket not found, it's an error
            else:
                SRTError('Ticket not found: 예약 내역을 확인하세요')
        else:
            raise SRTResponseError(parser.message())

    def get_reservations(self):
        if not self.is_login:
            raise SRTNotLoggedInError()

        url = SRT_TICKETS
        data = SRTRequestData()
        data.update_datasets({
            'pageNo': '0',
            'MB_CRD_NO': self.user_membership_number,
            'KR_JSESSIONID': self.kr_session_id,
            'SR_JSESSIONID': self.sr_session_id,
        })

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)
        reservation_data = parser.get_data1()
        train_data = parser.get_data2()
        if parser.success():
            self._log(parser.message())
            reservations = []
            for r, d in zip(reservation_data, train_data):
                tickets = self._ticket_info(r['pnrNo'])
                reservation = SRTReservation(r, d, tickets)
                reservations.append(reservation)

            return reservations
        else:
            raise SRTResponseError(parser.message())

    def _ticket_info(self, reservation_id):
        if not self.is_login:
            raise SRTNotLoggedInError()

        url = SRT_TICKET_INFO
        data = SRTRequestData()
        data.update_datasets({
            'pnrNo': reservation_id,
            'jrnySqno': '1',
            'MB_CRD_NO': self.user_membership_number,
            'KR_JSESSIONID': self.kr_session_id,
            'SR_JSESSIONID': self.sr_session_id,
        })

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)
        tickets_data = parser.get_data1()
        if parser.success():
            self._log(parser.message())
            tickets = []
            for data in tickets_data:
                tickets.append(SRTTicket(data))
            return tickets
        else:
            raise SRTResponseError(parser.message())

    def cancel(self, reservation):
        if not self.is_login:
            raise SRTNotLoggedInError()

        if isinstance(reservation, SRTReservation):
            reservation = reservation.reservation_number

        url = SRT_CANCEL
        data = SRTRequestData()
        data.update_datasets({
            'pnrNo': reservation,
            'MB_CRD_NO': self.user_membership_number,
            'KR_JSESSIONID': self.kr_session_id,
            'SR_JSESSIONID': self.sr_session_id,
        })

        r = self._session.post(url=url, data=data.dump().encode('utf-8'))
        parser = SRTResponseData(r.text)

        if parser.success():
            self._log(parser.message())
        else:
            raise SRTResponseError(parser.message())
