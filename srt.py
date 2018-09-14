import re
import requests

EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
PHONE_NUMBER_REGEX = re.compile(r'\d{11}')

SCHEME = 'https'
SRT_HOST = 'app.srail.co.kr'
SRT_PORT = '443'

SRT_MOBILE = '{scheme}://{host}:{port}'.format(scheme=SCHEME, host=SRT_HOST, port=SRT_PORT)
SRT_LOGIN = '{}/apb/selectListApb01080.do'.format(SRT_MOBILE)


DEFAULT_HEADERS = {
    'User-Agent': 'nexacroplatform14-android/2014 (compatible; Mozilla/4.0; MSIE 7.0)',
    'Referer': 'file:///data/user/0/kr.co.srail.app/files/NEXACRO/APB/APB0101C.xfdl.js',
}

LOGIN_DATA='''<?xml version="1.0" encoding="UTF-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset">
    <Parameters>
        <Parameter id="gs_loginCrdNo">0000000000</Parameter>
        <Parameter id="WMONID">GIAgiHeSKoy</Parameter>
        <Parameter id="JSESSIONID_ETK_MB">aePnNKXlIr7s4SaoLWXespn0vz0Rj65h0YErV7akiKgf2aTp0Z6MHd1Y5yQAeRGb.ZXRrcC9FVEtfTUJDT04wMi0x</Parameter>
    </Parameters>
    <Dataset id="dsInput1">
        <ColumnInfo>
            <Column id="srchDvCd" type="STRING" size="256"  />
            <Column id="srchDvNm" type="STRING" size="256"  />
            <Column id="hmpgPwdCphd" type="STRING" size="256"  />
            <Column id="deviceKey" type="STRING" size="256"  />
            <Column id="deviceInfo" type="STRING" size="256"  />
            <Column id="mobileproducttype" type="STRING" size="256"  />
        </ColumnInfo>
        <Rows>
            <Row>
                <Col id="srchDvCd">{login_type}</Col>
                <Col id="srchDvNm">{srt_id}</Col>
                <Col id="hmpgPwdCphd">{srt_pw}</Col>
                <Col id="deviceKey">AEE7D49B23CF5FAE</Col>
                <Col id="deviceInfo">Android&#32;8.0.0</Col>
                <Col id="mobileproducttype">LM-G710N</Col>
            </Row>
        </Rows>
    </Dataset>
    <Dataset id="__DS_PARAM_INFO__">
        <ColumnInfo />
        <Rows>
        </Rows>
    </Dataset>
    <Dataset id="__DS_TRANS_INFO__">
        <ColumnInfo>
            <Column id="strSvcID" type="STRING" size="256"  />
            <Column id="strURL" type="STRING" size="256"  />
            <Column id="strInDatasets" type="STRING" size="256"  />
            <Column id="strOutDatasets" type="STRING" size="256"  />
            <Column id="strOS" type="STRING" size="256"  />
            <Column id="strDeviceInfo" type="STRING" size="256"  />
        </ColumnInfo>
        <Rows>
            <Row>
                <Col id="strSvcID">login</Col>
                <Col id="strURL">apb/selectListApb01080.do</Col>
                <Col id="strInDatasets">dsInput1</Col>
                <Col id="strOutDatasets">dsOutput0&#32;ds_outCmc</Col>
                <Col id="strOS">Android</Col>
                <Col id="strDeviceInfo">Android&#32;8.0.0&#32;LM-G710N</Col>
            </Row>
        </Rows>
    </Dataset>
    <Dataset id="gds_userInfo">
        <ColumnInfo>
            <Column id="CUST_MG_NO" type="STRING" size="256"  />
            <Column id="MB_CRD_NO" type="STRING" size="256"  />
            <Column id="CUST_NM" type="STRING" size="256"  />
            <Column id="CUST_SRT_CD" type="STRING" size="256"  />
            <Column id="CUST_CL_CD" type="STRING" size="256"  />
            <Column id="BTDT" type="STRING" size="256"  />
            <Column id="SEX_DV_CD" type="STRING" size="256"  />
            <Column id="ABRD_RS_STN_CD" type="STRING" size="256"  />
            <Column id="GOFF_RS_STN_CD" type="STRING" size="256"  />
            <Column id="DSCP_YN" type="STRING" size="256"  />
            <Column id="USR_PWD_CPHD" type="STRING" size="256"  />
            <Column id="USER_DV" type="STRING" size="256"  />
            <Column id="MBL_PHONE" type="STRING" size="256"  />
            <Column id="USER_KEY" type="STRING" size="256"  />
            <Column id="KR_JSESSIONID" type="STRING" size="256"  />
            <Column id="SR_JSESSIONID" type="STRING" size="256"  />
            <Column id="DPT_NM" type="STRING" size="256"  />
            <Column id="POSI_NM" type="STRING" size="256"  />
            <Column id="GRD_NM" type="STRING" size="256"  />
        </ColumnInfo>
        <Rows>
            <Row>
            </Row>
        </Rows>
    </Dataset>
    <Dataset id="gds_pageInfo">
        <ColumnInfo>
            <Column id="PAGE_LINE" type="STRING" size="256"  />
            <Column id="CURR_PAGE" type="STRING" size="256"  />
        </ColumnInfo>
        <Rows>
            <Row>
                <Col id="PAGE_LINE" />
                <Col id="CURR_PAGE" />
            </Row>
        </Rows>
    </Dataset>
</Root>
'''


class SRT:
    """SRT object"""

    def __init__(self, srt_id, srt_pw, auto_login=True, want_feedback=False):
        self._session = requests.session()
        self._session.headers.update(DEFAULT_HEADERS)

        self.srt_id = srt_id
        self.srt_pw = srt_pw
        self.feedback = want_feedback
        self.is_login = False

        if auto_login:
            self.login(srt_id, srt_pw)

    def login(self, srt_id=None, srt_pw=None):

        if srt_id is None:
            srt_id = self.srt_id
        else:
            self.srt_id = srt_id

        if srt_pw is None:
            srt_pw = self.srt_pw
        else:
            self.srt_pw = srt_pw

        if EMAIL_REGEX.match(srt_id):
            login_type = '2'
        elif PHONE_NUMBER_REGEX.match(srt_id):
            login_type = '3'
        else: # membership id login
            login_type = '1'

        url = SRT_LOGIN
        r = self._session.post(url=url,
                               data=LOGIN_DATA.format(
                                   login_type=login_type, srt_id=srt_id, srt_pw=srt_pw,
                               ))

        print(r.text)