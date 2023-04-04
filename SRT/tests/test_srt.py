import os
from datetime import datetime, timedelta

import pytest

from SRT import SRT, SRTLoginError


@pytest.fixture(scope="module")
def srt():
    try:
        username = os.environ["SRT_USERNAME"]
        password = os.environ["SRT_PASSWORD"]
    except KeyError:
        pytest.fail(KeyError("You should specify SRT_USERNAME and SRT_PASSWORD"))

    return SRT(username, password)


def test_login_success(srt):
    srt.login()


def test_login_fail():
    username = "010-1234-5678"
    wrong_password = "deadbeef"

    with pytest.raises(SRTLoginError):
        SRT(username, wrong_password)


def test_search_train(srt):
    dep = "수서"
    arr = "부산"
    time = "000000"
    time_limit = "120000"
    date = (datetime.now() + timedelta(days=3)).strftime("%Y%m%d")

    trains = srt.search_train(dep, arr, date, time, time_limit, available_only=False)
    assert len(trains) != 0


def test_get_reservations(srt):
    srt.get_reservations()


def test_reserve_and_cancel(srt, pytestconfig):
    pytestconfig.getoption("--full", skip=True)
    dep = "수서"
    arr = "대전"
    time = "000000"

    # loop until empty seat is found
    reservation = None
    for day in range(5, 30):
        date = (datetime.now() + timedelta(days=day)).strftime("%Y%m%d")

        trains = srt.search_train(dep, arr, date, time)

        assert len(trains) != 0

        for train in trains:
            if train.general_seat_available():
                reservation = srt.reserve(train)
                break

        if reservation is not None:
            break

    if reservation is None:
        pytest.warns(Warning("Empty seat not found, skipping reservation test"))

    srt.cancel(reservation)
