import xml.etree.ElementTree as ET

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
            
            <Column id="grpDv" type="STRING" size="256"  />
            <Column id="jobId" type="STRING" size="256"  />
            <Column id="rtnDv" type="STRING" size="256"  />
            <Column id="jrnyTpCd" type="STRING" size="256"  />
            <Column id="jrnyCnt" type="STRING" size="256"  />
            <Column id="totPrnb" type="STRING" size="256"  />
            <Column id="totPrnbNm" type="STRING" size="256"  />
            <Column id="stndFlg" type="STRING" size="256"  />
            <Column id="jrnySqno1" type="STRING" size="256"  />
            <Column id="runDt1" type="STRING" size="256"  />
            <Column id="trnNo1" type="STRING" size="256"  />
            <Column id="trnGpCd1" type="STRING" size="256"  />
            <Column id="trnGpNm1" type="STRING" size="256"  />
            <Column id="stlbTrnClsfCd1" type="STRING" size="256"  />
            <Column id="dptDt1" type="STRING" size="256"  />
            <Column id="dptTm1" type="STRING" size="256"  />
            <Column id="dptDtTmNm1" type="STRING" size="256"  />
            <Column id="dptRsStnCd1" type="STRING" size="256"  />
            <Column id="dptRsStnCdNm1" type="STRING" size="256"  />
            <Column id="dptStnConsOrdr1" type="STRING" size="256"  />
            <Column id="dptStnRunOrdr1" type="STRING" size="256"  />
            <Column id="arvRsStnCd1" type="STRING" size="256"  />
            <Column id="arvRsStnCdNm1" type="STRING" size="256"  />
            <Column id="arvStnConsOrdr1" type="STRING" size="256"  />
            <Column id="arvStnRunOrdr1" type="STRING" size="256"  />
            <Column id="scarGridcnt1" type="STRING" size="256"  />
            <Column id="scarNo1" type="STRING" size="256"  />
            <Column id="scarNoNm1" type="STRING" size="256"  />
            <Column id="seatNo1_1" type="STRING" size="256"  />
            <Column id="seatNo1_2" type="STRING" size="256"  />
            <Column id="seatNo1_3" type="STRING" size="256"  />
            <Column id="seatNo1_4" type="STRING" size="256"  />
            <Column id="seatNo1_5" type="STRING" size="256"  />
            <Column id="seatNo1_6" type="STRING" size="256"  />
            <Column id="seatNo1_7" type="STRING" size="256"  />
            <Column id="seatNo1_8" type="STRING" size="256"  />
            <Column id="seatNo1_9" type="STRING" size="256"  />
            <Column id="smkSeatAttCd1" type="STRING" size="256"  />
            <Column id="dirSeatAttCd1" type="STRING" size="256"  />
            <Column id="locSeatAttCd1" type="STRING" size="256"  />
            <Column id="rqSeatAttCd1" type="STRING" size="256"  />
            <Column id="etcSeatAttCd1" type="STRING" size="256"  />
            <Column id="seatAttNm1" type="STRING" size="256"  />
            <Column id="jrnySqno2" type="STRING" size="256"  />
            <Column id="runDt2" type="STRING" size="256"  />
            <Column id="trnNo2" type="STRING" size="256"  />
            <Column id="trnGpCd2" type="STRING" size="256"  />
            <Column id="stlbTrnClsfCd2" type="STRING" size="256"  />
            <Column id="dptDt2" type="STRING" size="256"  />
            <Column id="dptTm2" type="STRING" size="256"  />
            <Column id="dptDtTmNm2" type="STRING" size="256"  />
            <Column id="dptRsStnCd2" type="STRING" size="256"  />
            <Column id="dptRsStnCdNm2" type="STRING" size="256"  />
            <Column id="dptStnConsOrdr2" type="STRING" size="256"  />
            <Column id="dptStnRunOrdr2" type="STRING" size="256"  />
            <Column id="arvRsStnCd2" type="STRING" size="256"  />
            <Column id="arvRsStnCdNm2" type="STRING" size="256"  />
            <Column id="arvStnConsOrdr2" type="STRING" size="256"  />
            <Column id="arvStnRunOrdr2" type="STRING" size="256"  />
            <Column id="scarGridcnt2" type="STRING" size="256"  />
            <Column id="scarNo2" type="STRING" size="256"  />
            <Column id="scarNoNm2" type="STRING" size="256"  />
            <Column id="seatNo2_1" type="STRING" size="256"  />
            <Column id="seatNo2_2" type="STRING" size="256"  />
            <Column id="seatNo2_3" type="STRING" size="256"  />
            <Column id="seatNo2_4" type="STRING" size="256"  />
            <Column id="seatNo2_5" type="STRING" size="256"  />
            <Column id="seatNo2_6" type="STRING" size="256"  />
            <Column id="seatNo2_7" type="STRING" size="256"  />
            <Column id="seatNo2_8" type="STRING" size="256"  />
            <Column id="seatNo2_9" type="STRING" size="256"  />
            <Column id="smkSeatAttCd2" type="STRING" size="256"  />
            <Column id="dirSeatAttCd2" type="STRING" size="256"  />
            <Column id="locSeatAttCd2" type="STRING" size="256"  />
            <Column id="rqSeatAttCd2" type="STRING" size="256"  />
            <Column id="etcSeatAttCd2" type="STRING" size="256"  />
            <Column id="seatAttNm2" type="STRING" size="256"  />
            <Column id="psgGridcnt" type="STRING" size="256"  />
            <Column id="psgTpCd1" type="STRING" size="256"  />
            <Column id="psgInfoPerPrnb1" type="STRING" size="256"  />
            <Column id="psgTpCd2" type="STRING" size="256"  />
            <Column id="psgInfoPerPrnb2" type="STRING" size="256"  />
            <Column id="psgTpCd3" type="STRING" size="256"  />
            <Column id="psgInfoPerPrnb3" type="STRING" size="256"  />
            <Column id="psgTpCd4" type="STRING" size="256"  />
            <Column id="psgInfoPerPrnb4" type="STRING" size="256"  />
            <Column id="psgTpCd5" type="STRING" size="256"  />
            <Column id="psrmClCd1" type="STRING" size="256"  />
            <Column id="psrmClNm1" type="STRING" size="256"  />
            <Column id="psrmClCd2" type="STRING" size="256"  />
            <Column id="psrmClNm2" type="STRING" size="256"  />
            <Column id="psgInfoPerPrnb5" type="STRING" size="256"  />
            <Column id="back_dptDt1" type="STRING" size="256"  />
            <Column id="back_dptTm1" type="STRING" size="256"  />
            <Column id="back_dptDtTmNm1" type="STRING" size="256"  />
            <Column id="back_dptDt2" type="STRING" size="256"  />
            <Column id="back_dptTm2" type="STRING" size="256"  />
            <Column id="back_dptDtTmNm2" type="STRING" size="256"  />
            <Column id="go_baseDsXml" type="STRING" size="256"  />
            <Column id="go_seatDsXml" type="STRING" size="256"  />
            <Column id="mutMrkVrfCd" type="STRING" size="256"  />
            <Column id="koYn" type="STRING" size="256"  />
            
            <Column id="ctlDvCd" type="STRING" size="256"  />
            <Column id="pageNo" type="STRING" size="256"  />
            <Column id="telno1" type="STRING" size="256"  />
            <Column id="telno2" type="STRING" size="256"  />
            <Column id="telno3" type="STRING" size="256"  />
            <Column id="custNm" type="STRING" size="256"  />
            <Column id="nonMbPwd" type="STRING" size="256"  />
            <Column id="abrdDtFrom" type="STRING" size="256"  />
            <Column id="abrdDtTo" type="STRING" size="256"  />
            <Column id="deviceId" type="STRING" size="256"  />
            
            <Column id="pnrNo" type="STRING" size="256"  />
            <Column id="jrnySqno" type="STRING" size="256"  />
            <Column id="chgTrnDvCd" type="STRING" size="256"  />
            <Column id="rsvChgTno" type="STRING" size="256"  />
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
                <Col id="trnNo"></Col>
                
                <Col id="grpDv">0</Col>
                <Col id="jobId">1101</Col>
                <Col id="rtnDv">0</Col>
                <Col id="jrnyTpCd">11</Col>
                <Col id="jrnyCnt">1</Col>
                <Col id="totPrnb"></Col>
                <Col id="totPrnbNm"></Col>
                <Col id="stndFlg">N</Col>
                <Col id="jrnySqno1">001</Col>
                <Col id="runDt1"></Col>
                <Col id="trnNo1"></Col>
                <Col id="trnGpCd1">300</Col>
                <Col id="trnGpNm1">전체</Col>
                <Col id="stlbTrnClsfCd1">17</Col>
                <Col id="dptDt1"></Col>
                <Col id="dptTm1"></Col>
                <Col id="dptDtTmNm1"></Col>
                <Col id="dptRsStnCd1"></Col>
                <Col id="dptRsStnCdNm1"></Col>
                <Col id="dptStnConsOrdr1"></Col>
                <Col id="dptStnRunOrdr1"></Col>
                <Col id="arvRsStnCd1"></Col>
                <Col id="arvRsStnCdNm1"></Col>
                <Col id="arvStnConsOrdr1"></Col>
                <Col id="arvStnRunOrdr1"></Col>
                <Col id="smkSeatAttCd1">000</Col>
                <Col id="dirSeatAttCd1">009</Col>
                <Col id="locSeatAttCd1"></Col>
                <Col id="rqSeatAttCd1"></Col>
                <Col id="etcSeatAttCd1">000</Col>
                <Col id="seatAttNm1"></Col>
                <Col id="smkSeatAttCd2"></Col>
                <Col id="dirSeatAttCd2"></Col>
                <Col id="locSeatAttCd2"></Col>
                <Col id="rqSeatAttCd2"></Col>
                <Col id="etcSeatAttCd2"></Col>
                <Col id="seatAttNm2"></Col>
                <Col id="psgGridcnt"></Col>
                <Col id="psgTpCd1"></Col>
                <Col id="psgInfoPerPrnb1"></Col>
                <Col id="psgTpCd2" />
                <Col id="psgInfoPerPrnb2"></Col>
                <Col id="psgTpCd3" />
                <Col id="psgInfoPerPrnb3"></Col>
                <Col id="psgTpCd4" />
                <Col id="psgInfoPerPrnb4"></Col>
                <Col id="psgTpCd5" />
                <Col id="psrmClCd1"></Col>
                <Col id="psgInfoPerPrnb5"></Col>
                <Col id="back_dptDt1"></Col>
                <Col id="back_dptTm1"></Col>
                <Col id="back_dptDtTmNm1"></Col>
                <Col id="go_baseDsXml" />
                <Col id="go_seatDsXml" />
                
                <Col id="pageNo"></Col>
                
                <Col id="pnrNo"></Col>
                <Col id="jrnySqno"></Col>
                <Col id="chgTrnDvCd"></Col>
                <Col id="rsvChgTno"></Col>
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
