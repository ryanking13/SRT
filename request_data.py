import xml.etree.ElementTree as ET
import errors

XML_BASE = '''<?xml version="1.0" encoding="UTF-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset">
    <Parameters>
        <Parameter id="gs_loginCrdNo">0000000000</Parameter>
        <Parameter id="WMONID">GIAgiHeSKoy</Parameter>
        <Parameter id="JSESSIONID_ETK_MB">JBSJhvuZkDxNyji1FcgPe2u1o0eSHZe10NWFG5NqUFkjptQo0C2he1VD5uWTbMlp.ZXRrcC9FVEtfTUJDT04wMi0x</Parameter>
    </Parameters>
    <Dataset id="dsInput1">
        <ColumnInfo>
            <Column id="srchDvCd" type="STRING" size="256"  />
            <Column id="srchDvNm" type="STRING" size="256"  />
            <Column id="hmpgPwdCphd" type="STRING" size="256"  />
            <Column id="deviceKey" type="STRING" size="256"  />
            <Column id="deviceInfo" type="STRING" size="256"  />
            <Column id="mobileproducttype" type="STRING" size="256"  />
            <Column id="chtnDvCd" type="STRING" size="256"  />
            <Column id="dptDt" type="STRING" size="256"  />
            <Column id="dptTm" type="STRING" size="256"  />
            <Column id="dptRsStnCd" type="STRING" size="256"  />
            <Column id="dptRsStnCdNm" type="STRING" size="256"  />
            <Column id="arvRsStnCd" type="STRING" size="256"  />
            <Column id="stlbTrnClsfCd" type="STRING" size="256"  />
            <Column id="trnGpCd" type="STRING" size="256"  />
            <Column id="psgNum" type="STRING" size="256"  />
            <Column id="seatAttCd" type="STRING" size="256"  />
            <Column id="arriveTime" type="STRING" size="256"  />
            <Column id="trnNo" type="STRING" size="256"  />
        </ColumnInfo>
        <Rows>
            <Row>
                <Col id="srchDvCd"></Col>
                <Col id="srchDvNm"></Col>
                <Col id="hmpgPwdCphd"></Col>
                <Col id="deviceKey"></Col>
                <Col id="deviceInfo"></Col>
                <Col id="mobileproducttype"></Col>
                <Col id="chtnDvCd"></Col>
                <Col id="dptDt"></Col>
                <Col id="dptTm"></Col>
                <Col id="dptRsStnCd"></Col>
                <Col id="dptRsStnCdNm"></Col>
                <Col id="arvRsStnCd"></Col>
                <Col id="stlbTrnClsfCd"></Col>
                <Col id="trnGpCd"></Col>
                <Col id="psgNum"></Col>
                <Col id="seatAttCd"></Col>
                <Col id="arriveTime"></Col>
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
                <Col id="strSvcID"></Col>
                <Col id="strURL"></Col>
                <Col id="strInDatasets">dsInput1</Col>
                <Col id="strOutDatasets">dsOutput0&#32;ds_outCmc</Col>
                <Col id="strOS"></Col>
                <Col id="strDeviceInfo"></Col>
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
                <Col id="CUST_MG_NO"></Col>
                <Col id="MB_CRD_NO"></Col>
                <Col id="CUST_NM"></Col>
                <Col id="CUST_SRT_CD"></Col>
                <Col id="CUST_CL_CD"></Col>
                <Col id="BTDT"></Col>
                <Col id="SEX_DV_CD"></Col>
                <Col id="ABRD_RS_STN_CD"></Col>
                <Col id="GOFF_RS_STN_CD"></Col>
                <Col id="DSCP_YN"></Col>
                <Col id="USR_PWD_CPHD"></Col>
                <Col id="USER_DV"></Col>
                <Col id="MBL_PHONE"></Col>
                <Col id="USER_KEY"></Col>
                <Col id="KR_JSESSIONID"></Col>
                <Col id="SR_JSESSIONID"></Col>
                <Col id="DPT_NM"></Col>
                <Col id="POSI_NM"></Col>
                <Col id="GRD_NM"></Col>
            </Row>
        </Rows>
    </Dataset>
</Root>
'''


class SRTRequestData:
    """SRT Request data class
    dinamically construct XML data for API request
    """

    XML_PREFIX = '<?xml version="1.0" encoding="UTF-8"?>\n'
    NAMESPACE = '{http://www.nexacroplatform.com/platform/dataset}'
    DATASETTAG = NAMESPACE + 'Dataset'
    PARAMETERTAG = NAMESPACE + 'Parameter'
    DATATAG = NAMESPACE + 'Col'

    def __init__(self):
        # remove default ns0 prefix
        ET.register_namespace('', 'http://www.nexacroplatform.com/platform/dataset')
        
        self._xml = ET.fromstring(XML_BASE)

    def __str__(self):
        return self.dump()

    def dump(self):
        return self.XML_PREFIX + ET.tostring(self._xml, encoding='unicode')

    def _update(self, id, value, tag):
        for elem in self._xml.iter():
            if elem.tag == tag and elem.get('id') == id:
                elem.text = value
                return True
        else:
            raise KeyError('Tag id "{}" not exists in xml element'.format(id))

    def update_parameter(self, id, value):
        return self._update(id, value, self.PARAMETERTAG)

    def update_parameters(self, items):
        for k, v in items.items():
            self.update_parameter(k, v)

    def update_dataset(self, id, value):
        return self._update(id, value, self.DATATAG)

    def update_datasets(self, items):
        for k, v in items.items():
            self.update_dataset(k, v)

    def update(self, id, value, tag_type='dataset'):
        if tag_type == 'dataset':
            return self.update_dataset(id, value)
        elif tag_type == 'parameter':
            return self.update_parameter(id, value)
        else:
            raise ValueError('tag_type must be dataset or parameter')