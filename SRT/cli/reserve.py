import os
from datetime import datetime, timedelta

from PyInquirer import prompt

from SRT import SRT

VERBOSE = os.environ.get("DEBUG") is not None

SRT_STATIONS = (
    "수서",
    "동탄",
    "지제",
    "천안아산",
    "오송",
    "대전",
    "공주",
    "익산",
    "정읍",
    "광주송정",
    "나주",
    "목포",
    "김천구미",
    "서대구",
    "동대구",
    "신경주",
    "울산(통도사)",
    "부산",
)

not_empty = lambda s: len(s) > 0


def hi():
    print(
        """
░██████╗██████╗░████████╗
██╔════╝██╔══██╗╚══██╔══╝
╚█████╗░██████╔╝░░░██║░░░
░╚═══██╗██╔══██╗░░░██║░░░
██████╔╝██║░░██║░░░██║░░░
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░
"""
    )


def login():
    questions = [
        {
            "type": "input",
            "name": "username",
            "message": "SRT ID (username, e-mail, phone):",
            "validate": not_empty,
        },
        {
            "type": "password",
            "name": "password",
            "message": "SRT Password:",
            "validate": not_empty,
        },
    ]

    inputs = prompt(questions)
    return SRT(inputs["username"], inputs["password"], verbose=VERBOSE)


def select_station():
    questions = [
        {
            "type": "list",
            "name": "dep",
            "message": "출발역:",
            "choices": SRT_STATIONS,
        },
        {
            "type": "list",
            "name": "arr",
            "message": "도착역:",
            "choices": SRT_STATIONS,
        },
    ]

    stations = prompt(questions)
    return stations["dep"], stations["arr"]


def select_date():
    next_cnt = 0
    num_days = 10
    to_prev = "이전 날짜로"
    to_next = "다음 날짜로"

    while True:
        not_first = next_cnt > 0

        start_date = datetime.now() + timedelta(days=next_cnt * num_days)
        dates = [
            (start_date + timedelta(days=i)).strftime("%Y%m%d") for i in range(num_days)
        ]

        if not_first:
            dates = [to_prev] + dates

        dates += [to_next]

        questions = [
            {
                "type": "list",
                "name": "date",
                "message": "출발 날짜:",
                "choices": dates,
            }
        ]

        date = prompt(questions)["date"]

        if date == to_prev:
            next_cnt -= 1
            continue
        elif date == to_next:
            next_cnt += 1
            continue
        else:
            return date


def search_train(client, dep, arr, date):

    trains = client.search_train(dep, arr, date, "000000")
    trains = [
        {
            "name": repr(train),
            "value": train,
        }
        for train in trains
    ]
    questions = [
        {
            "type": "list",
            "name": "train",
            "message": "열차 선택:",
            "choices": trains,
        },
    ]

    train = prompt(questions)["train"]
    return train


def reserve(client, train):
    return client.reserve(train)


def main():
    hi()

    srt = login()
    station_dep, station_arr = select_station()
    date_dep = select_date()

    train = search_train(srt, station_dep, station_arr, date_dep)
    reservation = reserve(srt, train)

    print("예약 완료! 홈페이지에서 결제를 완료하세요.")
    print(reservation)


if __name__ == "__main__":
    main()
