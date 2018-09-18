import xml.etree.ElementTree as ET

XML_BASE = '''<?xml version="1.0" encoding="UTF-8"?>
<Root xmlns="http://www.nexacroplatform.com/platform/dataset">
    <Parameters>
    </Parameters>
    <Dataset id="dsInput1">
        <ColumnInfo>
        </ColumnInfo>
        <Rows>
            <Row>
            </Row>
        </Rows>
    </Dataset>
    <Dataset id="__DS_TRANS_INFO__">
        <ColumnInfo>
        </ColumnInfo>
        <Rows>
            <Row>
            </Row>
        </Rows>
    </Dataset>
    <Dataset id="gds_userInfo">
        <ColumnInfo>
            <Column id="KR_JSESSIONID" type="STRING" size="256"  />
            <Column id="SR_JSESSIONID" type="STRING" size="256"  />
        </ColumnInfo>
        <Rows>
            <Row>
                <Col id="KR_JSESSIONID">{kr_session_id}</Col>
                <Col id="SR_JSESSIONID">{sr_session_id}</Col>
            </Row>
        </Rows>
    </Dataset>
</Root>
'''

class SRTRequestData:

    XML_PREFIX = '<?xml version="1.0" encoding="UTF-8"?>\n'
    NAMESPACE = '{http://www.nexacro.com/platform/dataset}'
    DATASETTAG = NAMESPACE + 'Dataset'
    PARAMETERTAG = NAMESPACE + 'Parameters'
    DATATAG = NAMESPACE + 'Col'

    def __init__(self):
        # remove default ns0 prefix
        ET.register_namespace('', 'http://www.nexacroplatform.com/platform/dataset')
        
        self._xml = ET.fromstring(XML_BASE)

    def __str__(self):
        return self.dump()

    def dump(self):
        return self.XML_PREFIX + ET.tostring(self._xml, encoding='unicode')

    def update_parameter(self, id, value):
        pass

    def update_dataset(self, id, value):
        pass

    def update(self, id, value, type='dataset'):
        pass

r = SRTRequestData()
print(r)
