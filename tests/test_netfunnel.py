from SRT.netfunnel import NetFunnelHelper, NetFunnelResponse


def test_get_netfunnel_key_success():
    helper = NetFunnelHelper()
    helper._get_netfunnel_key(False)


def test_set_complete_success():
    helper = NetFunnelHelper()
    key = helper._get_netfunnel_key(False)
    helper._set_complete(key)


def test_netfunnel_response_parse():
    key = "C75890BD44561ED79DFA180832F2D016F95C9F7BE965B2"
    response_text = f"""
NetFunnel.gRtype=5101;
NetFunnel.gControl.result='5002:200:key={key}&nwait=0&nnext=0&tps=0&ttl=0&ip=nf.letskorail.com&port=443';
NetFunnel.gControl._showResult();
"""
    response = NetFunnelResponse.parse(response_text)
    assert "key" in response.data
    assert response.data["key"] == key
    assert response.data["nwait"] == "0"
    assert response.data["nnext"] == "0"
    assert response.data["tps"] == "0"
    assert response.data["ttl"] == "0"
    assert response.data["ip"] == "nf.letskorail.com"
    assert response.data["port"] == "443"
    assert response.data["opcode"] == "5101"
    assert response.data["next_code"] == "5002"
    assert response.data["status"] == "200"

    response_text = """
NetFunnel.gRtype=5002;
NetFunnel.gControl.result='5002:200:key=test_key&nwait=0&nnext=0&tps=0&ttl=0&ip=nf.letskorail.com&port=443';
NetFunnel.gControl._showResult();
"""

    response = NetFunnelResponse.parse(response_text)
    assert "key" in response.data
    assert response.data["key"] == "test_key"
    assert response.data["nwait"] == "0"
    assert response.data["nnext"] == "0"
    assert response.data["tps"] == "0"
    assert response.data["ttl"] == "0"
    assert response.data["ip"] == "nf.letskorail.com"
    assert response.data["port"] == "443"
    assert response.data["opcode"] == "5002"
    assert response.data["next_code"] == "5002"
    assert response.data["status"] == "200"

    response_text = """
NetFunnel.gRtype=5004;NetFunnel.gControl.result='5004:502:msg="Already Completed"'; NetFunnel.gControl._showResult();
"""

    response = NetFunnelResponse.parse(response_text)
    assert "key" not in response.data
    assert response.data["opcode"] == "5004"
    assert response.data["next_code"] == "5004"
    assert response.data["status"] == "502"
    assert response.data["msg"] == '"Already Completed"'
