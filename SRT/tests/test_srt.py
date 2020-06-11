import os
import pytest
import configparser
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


def test_login():
    config = configparser.ConfigParser()
    print(os.getcwd())
    config.read('dev_config.ini')

    username = config['DEFAULT']['SRT_USERNAME']
    password = config['DEFAULT']['SRT_PASSWORD']
    SRT(username, password)