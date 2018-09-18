import xml.etree.ElementTree as ET

NAMESPACE = '{http://www.nexacro.com/platform/dataset}'
DATASETTAG = NAMESPACE + 'Dataset'
DATATAG = NAMESPACE + 'Col'


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
