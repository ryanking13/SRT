from pathlib import Path
import pytest

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