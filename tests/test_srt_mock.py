from pathlib import Path

import pytest

from SRT.reservation import SRTReservation

mock_response_dir = Path(__file__).parent / "mock_responses"


@pytest.fixture
def mock_server(httpserver, monkeypatch):
    from SRT import constants

    endpoints = {
        "main": httpserver.url_for("/main"),
        "login": httpserver.url_for("/login"),
        "logout": httpserver.url_for("/logout"),
        "search_schedule": httpserver.url_for("/search_schedule"),
        "reserve": httpserver.url_for("/reserve"),
        "tickets": httpserver.url_for("/tickets"),
        "ticket_info": httpserver.url_for("/ticket_info"),
        "cancel": httpserver.url_for("/cancel"),
        "standby_option": httpserver.url_for("/standby_option"),
        "payment": httpserver.url_for("/payment"),
    }

    monkeypatch.setattr(
        constants,
        "API_ENDPOINTS",
        endpoints,
    )

    yield


def register_mock_response(httpserver, endpoint, filename, status=200):
    response = (mock_response_dir / filename).read_text(encoding="utf-8")
    httpserver.expect_oneshot_request(endpoint).respond_with_data(
        response,
        status=status,
        headers={"Content-Type": "application/json"},
    )


def test_login_success(mock_server, httpserver):
    from SRT import SRT

    register_mock_response(httpserver, "/login", "login_success.json")

    srt = SRT("010-1234-1234", "password")
    assert srt.is_login


def test_login_fail_wrong_password(mock_server, httpserver):
    from SRT import SRT, SRTLoginError

    register_mock_response(httpserver, "/login", "login_fail_password.json")

    with pytest.raises(SRTLoginError):
        SRT("010-1234-1234", "password")


def test_login_fail_wrong_username(mock_server, httpserver):
    from SRT import SRT, SRTLoginError

    register_mock_response(httpserver, "/login", "login_fail_no_user.json")

    with pytest.raises(SRTLoginError):
        SRT("010-1234-1234", "password")


def test_logout(mock_server, httpserver):
    from SRT import SRT

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(httpserver, "/logout", "logout_success.json")

    srt = SRT("010-1234-1234", "password")
    srt.logout()
    assert not srt.is_login


# 결제 테스트를 위한 mock reservation
mock_reservation = SRTReservation(
    {
        "pnrNo": "000000000",
        "tkSpecNum": "1",
        "rcvdAmt": "36900",
    },
    {
        "stlbTrnClsfCd": "00",
        "trnNo": "0000",
        "dptDt": "20231024",
        "dptTm": "000000",
        "dptRsStnCd": "0551",
        "arvTm": "000000",
        "arvRsStnCd": "0015",
        "iseLmtDt": "20231024",
        "iseLmtTm": "000000",
        "stlFlg": "N",
    },
    [
        {
            "scarNo": "1",
            "seatNo": "1",
            "psrmClCd": "1",
            "psgTpCd": "1",
            "rcvdAmt": "36900",
            "stdrPrc": "36900",
            "dcntPrc": "600",
        }
    ],
)


# 결제 성공
def test_pay_with_card_success(mock_server, httpserver):
    from SRT import SRT

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(httpserver, "/payment", "pay_with_card_success.json")

    srt = SRT("010-1234-1234", "password")

    assert srt.pay_with_card(
        mock_reservation,
        number="0000000000000000",
        password="12",
        validation_number="700101",
        expire_date="1221",
        installment=0,
        card_type="J",
    )


# 결제 실패 - 입력이 잘못되었습니다
def test_pay_with_card_fail_bad_request(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_bad_request.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="% 입력이 잘못되었습니다."):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 할부 불가 카드
def test_pay_with_card_fail_cant_installment(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_cant_installment.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="할부불가카드"):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 비밀번호 오류
def test_pay_with_card_fail_card_password(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_card_password.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(
        SRTResponseError,
        match="비밀번호오류<br><br>사용하신 각 신용카드사의 고객센터로 문의 바랍니다.",
    ):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 유효기간 경과 카드
def test_pay_with_card_fail_expired_card(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_expired_card.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="유효기간경과카드"):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 주민번호 또는 사업자번호 오류
def test_pay_with_card_fail_invalid_auth_number(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_invalid_auth_number.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="주민번호 또는 사업자번호 오류입니다."):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 카드번호 오류
def test_pay_with_card_fail_invalid_card_number(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_invalid_card_number.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="카드번호오류"):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 유효기간 입력 오류
def test_pay_with_card_fail_invalid_expiration_date(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_invalid_expiration_date.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="유효기간을 잘못입력하셨습니다."):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 취소된 예약
def test_pay_with_card_fail_invalid_reservation(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_invalid_reservation.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(
        SRTResponseError,
        match="취소된 여정이므로 발매할 수 없습니다.<br>비회원은 다시 예약하셔야합니다.",
    ):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 한도 초과
def test_pay_with_card_fail_over_limit(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(httpserver, "/payment", "pay_with_card_fail_over_limit.json")

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="사용한도초과"):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )


# 결제 실패 - 거래정지 카드
def test_pay_with_card_fail_suspension_card(mock_server, httpserver):
    from SRT import SRT, SRTResponseError

    register_mock_response(httpserver, "/login", "login_success.json")
    register_mock_response(
        httpserver, "/payment", "pay_with_card_fail_suspension_card.json"
    )

    srt = SRT("010-1234-1234", "password")

    with pytest.raises(SRTResponseError, match="거래정지카드"):
        srt.pay_with_card(
            mock_reservation,
            number="0000000000000000",
            password="12",
            validation_number="700101",
            expire_date="1221",
            installment=0,
            card_type="J",
        )
