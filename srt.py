from datetime import datetime
import re
import requests
from constants import STATION_CODE
import errors
from request_data import SRTRequestData
from response_data import SRTResponseData
from train import SRTTrain

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
PHONE_NUMBER_REGEX = re.compile(r'(\d{3})-(\d{3,4})-(\d{4})')

SCHEME = 'https'
SRT_HOST = 'app.srail.co.kr'
SRT_PORT = '443'

SRT_MOBILE = '{scheme}://{host}:{port}'.format(scheme=SCHEME, host=SRT_HOST, port=SRT_PORT)
SRT_LOGIN = '{}/apb/selectListApb01080.do'.format(SRT_MOBILE)
SRT_LOGOUT = '{}/apb/selectListApb01081.do'.format(SRT_MOBILE)
SRT_SEARCH_SCHEDULE = '{}/ara/selectListAra10007.do'.format(SRT_MOBILE)

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
            'strSvcID': 'login',
            'srchDvCd': login_type,
            'srchDvNm': srt_id,
            'hmpgPwdCphd': srt_pw,
        })

        r = self._session.post(url=url, data=data.dump())
        parser = SRTResponseData(r.text)

        if parser.success():
            status, result, data = parser.get_data()
            self.kr_session_id = status.get('KR_JSESSIONID')
            self.sr_session_id = status.get('SR_JSESSIONID')
            self.user_name = result.get('CUST_NM')
            self.user_membership_number = result.get('MB_CRD_NO')
            self.user_phone_number = result.get('MBL_PHONE')
            self.user_type = result.get('CUST_MG_SRT_NM')  # 개인고객 or ...
            self.user_level = result.get('CUST_DTL_SRT_NM')  # 일반회원 or ...
            self.user_sex = result.get('SEX_CDV_NM')
            self._session.cookies.update({'gs_loginCrdNo': result.get('MB_CRD_NO')})

            self._log(parser.message())
            self.is_login = True
            return True

        else:
            self.is_login = False
            raise errors.SRTResponseError(parser.message())

    def logout(self):
        if not self.is_login:
            return

        url = SRT_LOGOUT
        data = SRTRequestData()
        data.update_datasets({
            'strSvcID': 'login',
            'KR_JSESSIONID': self.kr_session_id,
            'SR_JSESSIONID': self.sr_session_id,
        })

        r = self._session.post(url=url, data=data.dump())
        parser = SRTResponseData(r.text)

        if parser.success():
            self._log(parser.message())
            self.is_login = False
            return True
        else:
            raise errors.SRTResponseError(parser.message())

    def search_train(self, dep, arr, date=None, time=None):
        if not self.is_login:
            raise errors.SRTNotLoggedInError()

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
        status, result, data = parser.get_data()

        if parser.success():
            self._log(parser.message())
            trains = []
            for d in data:
                trains.append(SRTTrain(d))
            print(trains)
        else:
            raise errors.SRTResponseError(parser.message())


f = open('login_info.txt', 'r')
username = f.readline().strip()
password = f.readline().strip()
f.close()

s = SRT(username, password, verbose=True)
s.search_train(dep='수서', arr='부산', date='20180924', time='000000')