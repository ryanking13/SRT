from SRT import SRT
from SRT.train import SRTTrain
import time as tt
import random as rd
import sys
import os

ID = '아이디'
PASSWORD = '비밀번호'
DEPARTURE = '익산'
ARRIVAL = '수서'
TARGET_DATE = '20240918'
START_TIME = '140000'
LIMIT_TIME = '220000'

def play_sound():
    sound_file = '../Sound/sound1.mp3'
    os.system(f'afplay {sound_file}')

def search_possible_train(srt, dep, arr, date, time, time_limit) -> list[SRTTrain]:

    search_message = ["[SRT] Searching.","[SRT] Searching..","[SRT] Searching...","[SRT] Searching....","[SRT] Searching....."]
    index = 0

    while True:
        tt.sleep(rd.uniform(0.2, 1.5)) #랜덤 타임 휴식 (없으면 밴당함 ㅠ)
        available_train = srt.search_train(dep, arr, date, time, time_limit, True)

        sys.stdout.write("\r" + search_message[index])
        sys.stdout.flush()
        index = (index + 1) % len(search_message)

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
    limit = LIMIT_TIME

    first_available_train = reserve_train_until_success(srt, dep, arr, date, time, limit)


    reservation = srt.reserve(first_available_train)

    play_sound()
    print("결재를 완료해주세요")

