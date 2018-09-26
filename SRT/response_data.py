import xml.etree.ElementTree as ET
from .errors import *


class SRTResponseData():
    """SRT Response data class
    parse XML response from API request
    """

    NAMESPACE = '{http://www.nexacro.com/platform/dataset}'
    DATASETTAG = NAMESPACE + 'Dataset'
    DATATAG = NAMESPACE + 'Col'
    ROWTAG = NAMESPACE + 'Row'

    STATUS_OUTPUT_ID = 'dsOutput0'
    RESULT_OUTPUT_ID = 'dsCmcOutput0'
    DATA1_OUTPUT_ID = 'dsOutput1'
    DATA2_OUTPUT_ID = 'dsOutput2'

    STATUS_SUCCESS = 'SUCC'
    STATUS_FAIL = 'FAIL'

    def __init__(self, response):
        self._xml = ET.fromstring(response)
        self._status = {}
        self._result = {}
        self._data1 = []
        self._data2 = []

        # parse response data
        self._parse()

    def __str__(self):
        return self.dump()

    def dump(self):
        return ET.tostring(self._xml, encoding='unicode')

    def _parse(self):
        datasets = filter(lambda e: e.tag == self.DATASETTAG, list(self._xml))
        for dataset in datasets:
            tag_id = dataset.get('id')

            # status check
            if tag_id == self.STATUS_OUTPUT_ID:
                for row in dataset.iter(self.DATATAG):
                    self._status[row.get('id')] = row.text

            # result check
            elif tag_id == self.RESULT_OUTPUT_ID:
                for row in dataset.iter(self.DATATAG):
                    self._result[row.get('id')] = row.text

            # data check
            elif tag_id == self.DATA1_OUTPUT_ID:
                for row in dataset.iter(self.ROWTAG):
                    self._data1.append({})
                    for col in row.iter(self.DATATAG):
                        self._data1[-1][col.get('id')] = col.text

            # data check
            elif tag_id == self.DATA2_OUTPUT_ID:
                for row in dataset.iter(self.ROWTAG):
                    self._data2.append({})
                    for col in row.iter(self.DATATAG):
                        self._data2[-1][col.get('id')] = col.text

    def success(self):
        result = self._status.get('strResult', None)
        if result is None:
            raise SRTResponseError('Response status is not given')
        if result == self.STATUS_SUCCESS:
            return True
        elif result == self.STATUS_FAIL:
            return False
        else:
            raise SRTResponseError('Undefined result status "{}"'.format(result))

    def message(self):
        if 'MSG' in self._result:
            return self._result['MSG']
        elif 'msgTxt' in self._status:
            return self._status['msgTxt']
        else:
            return ''

    # get parse result
    def get_all(self):
        return self._status.copy(), self._result.copy(), self._data1.copy(), self._data2.copy()

    def get_status(self):
        return self._status.copy()

    def get_data1(self):
        return self._data1.copy()

    def get_data2(self):
        return self._data2.copy()
