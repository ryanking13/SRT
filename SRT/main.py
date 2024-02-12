from SRT import SRT
from SRT.train import SRTTrain
import time as tt
import random as rd

ID = '아이디'
PASSWORD = '비밀번호'
DEPARTURE = '출발지'
ARRIVAL = '도착지'
TARGET_DATE = '20240212출발일'
START_TIME = '080000검색시작시간'


def search_possible_train(srt, dep, arr, date, time, time_limit) -> list[SRTTrain]:
    while True:
        tt.sleep(rd.uniform(1, 2))
        available_train = srt.search_train(dep, arr, date, time, time_limit, True)
        if len(available_train) > 0:
            return available_train


def reserve_train_until_success(srt,
                                dep: str,
                                arr: str,
                                date: str | None = None,
                                time: str | None = None,
                                time_limit: str | None = None) -> SRTTrain:
    available_trains = search_possible_train(srt, dep, arr, date, time, time_limit)

    return available_trains[0]


if __name__ == '__main__':
    srt = SRT(ID, PASSWORD)  # 인스턴스 생성
    srt.login()
    dep = DEPARTURE
    arr = ARRIVAL
    date = TARGET_DATE
    time = START_TIME

    first_available_train = reserve_train_until_success(srt, dep, arr, date, time)

    reservation = srt.reserve(first_available_train)

    print("결재를 완료해주세요")

