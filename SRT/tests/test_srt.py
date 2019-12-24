import os
import pytest
from SRT import SRT, SRTLoginError


def test_login_success():
    username = os.environ["SRT_USERNAME"]
    password = os.environ["SRT_PASSWORD"]

    SRT(username, password)


def test_login_faile():
    username = os.environ["SRT_USERNAME"]
    wrong_password = "deadbeef"

    with pytest.raises(SRTLoginError):
        SRT(username, wrong_password)
