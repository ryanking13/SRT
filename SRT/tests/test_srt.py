import os
from datetime import datetime, timedelta

import pytest
from SRT import SRT, SRTLoginError

@pytest.fixture(scope="module")
def srt():
    username = os.environ["SRT_USERNAME"]
    password = os.environ["SRT_PASSWORD"]

    return SRT(username, password)


def test_login_success():
    srt.login()


def test_login_fail():
    username = os.environ["SRT_USERNAME"]
    wrong_password = "deadbeef"

    with pytest.raises(SRTLoginError):
        SRT(username, wrong_password)


def test_search_train():
    dep = "수서"
    arr = "부산"
    time = "000000"
    date = (datetime.now() + timedelta(days=3)).strftime("%Y%m%d")

    trains = srt.search_train(dep, arr, date, time)
    assert len(trains) != 0

