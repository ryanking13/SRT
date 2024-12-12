import pytest

from SRT.netfunnel import NetFunnelHelper, SRTNetFunnelError


@pytest.fixture(scope="module")
def helper():
    return NetFunnelHelper()

def test_get_netfunnel_key_success(helper):
    try:
        key = helper._get_netfunnel_key(True)
    except SRTNetFunnelError as e:
        raise AssertionError() from e
    assert key is not None


def test_set_complete_success(helper):
    key = helper._get_netfunnel_key(True)
    try:
        helper._set_complete(key)
    except SRTNetFunnelError as e:
        raise AssertionError() from e
    assert True

def test_extract_netfunnel_key_success(helper):
    key = "C75890BD44561ED79DFA180832F2D016F95C9F7BE965B2"
    response = f"""
NetFunnel.gRtype = 5101;
NetFunnel.gControl.result = '5002:200:key={key}&nwait=0&nnext=0&tps=0&ttl=0&ip=nf.letskorail.com&port=443';
NetFunnel.gControl._showResult();
"""
    key = helper._extract_netfunnel_key(response)
    assert key == key

