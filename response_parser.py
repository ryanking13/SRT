import xml.etree.ElementTree as ET

NAMESPACE = '{http://www.nexacro.com/platform/dataset}'
DATASETTAG = NAMESPACE + 'Dataset'
DATATAG = NAMESPACE + 'Col'


class SRTResponseData():
    NAMESPACE = '{http://www.nexacro.com/platform/dataset}'
    DATASETTAG = NAMESPACE + 'Dataset'
    DATATAG = NAMESPACE + 'Col'

    STATUS_OUTPUT_ID = 'dsOutput0'
    DATA_OUTPUT_ID = 'dsCmcOutput0'

    STATUS_SUCCESS = 'SUCC'
    STATUS_FAIL = 'FAIL'

    def __init__(self, response, auto_parse=True):
        self._xml = ET.fromstring(response)
        self._status = {}
        self._data = {}

        self._parsed = False
        if auto_parse:
            self._parse()

    def __str__(self):
        return self.dump()

    def dump(self):
        return self.XML_PREFIX + ET.tostring(self._xml, encoding='unicode')

    def _parse(self):
        datasets = filter(lambda e: e.tag == DATASETTAG, list(tree))
        for dataset in datasets:
            tag_id = dataset.get('id')

            # status check
            if tag_id == self.STATUS_OUTPUT_ID:
                for row in dataset.iter(DATATAG):
                    self._status[row.get('id')] = row.text

            # data check
            elif tag_id == self.DATA_OUTPUT_ID:
                for row in dataset.iter(DATATAG):
                    self._data[row.get('id')] = row.text

        self._parsed = True

    def success(self):
        result = status.get('strResult', None)
        if result is None:
            # TODO: raise error
            return False
        if result == self.STATUS_SUCCESS:
            return True
        elif result == self.STATUS_FAIL:
            return False
        else:
            # TODO: raise error
            return False


def parse_login(response):
    tree = ET.fromstring(response)
    datasets = filter(lambda e: e.tag == DATASETTAG, list(tree))

    status = {}
    data = {}
    for dataset in datasets:
        set_id = dataset.get('id')

        # status check
        if set_id == 'dsOutput0':
            for row in dataset.iter(DATATAG):
                status[row.get('id')] = row.text

        # data check
        elif set_id == 'dsCmcOutput0':
            for row in dataset.iter(DATATAG):
                data[row.get('id')] = row.text

    return status, data
