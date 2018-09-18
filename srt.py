import re
import requests
from request_data import SRTRequestData
import response_parser
import errors

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
PHONE_NUMBER_REGEX = re.compile(r'(\d{3})-(\d{3,4})-(\d{4})')

SCHEME = 'https'
SRT_HOST = 'app.srail.co.kr'
SRT_PORT = '443'

SRT_MOBILE = '{scheme}://{host}:{port}'.format(scheme=SCHEME, host=SRT_HOST, port=SRT_PORT)
SRT_LOGIN = '{}/apb/selectListApb01080.do'.format(SRT_MOBILE)
SRT_LOGOUT = '{}/apb/selectListApb01081.do'.format(SRT_MOBILE)

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

    def _error(self, msg):
        print('[-] ' + msg)

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
        status, data = response_parser.parse_login(r.text)
        result = status.get('strResult')

        if result == STATUS_SUCCESS:
            self.kr_session_id = status.get('KR_JSESSIONID')
            self.sr_session_id = status.get('SR_JSESSIONID')
            self.user_name = data.get('CUST_NM')
            self.user_membership_number = data.get('MB_CRD_NO')
            self.user_phone_number = data.get('MBL_PHONE')
            self.user_type = data.get('CUST_MG_SRT_NM')  # 개인고객 or ...
            self.user_level = data.get('CUST_DTL_SRT_NM')  # 일반회원 or ...
            self.user_sex = data.get('SEX_CDV_NM')
            self._session.cookies.update({'gs_loginCrdNo': data.get('MB_CRD_NO')})

            self._log(data.get('MSG'))
            self.is_login = True
            return True

        elif result == STATUS_FAIL:
            self._error(data.get('MSG'))
            self.is_login = False
            return False

        else:
            self.is_login = False
            raise errors.UndefinedResponseError(result)

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
        status, data = response_parser.parse_login(r.text)
        result = status.get('strResult')

        if result == STATUS_SUCCESS:
            self._log(status.get('msgTxt'))
            return True

        elif result == STATUS_FAIL:
            self._error(status.get('msgTxt'))
            self.is_login = False
            return False

        else:
            self.is_login = False
            raise errors.UndefinedResponseError(result)


f = open('login_info.txt', 'r')
username = f.readline().strip()
password = f.readline().strip()
f.close()

s = SRT(username, password, verbose=True)
s.logout()