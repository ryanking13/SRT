# SRT

![github actions badge](https://github.com/ryanking13/SRT/workflows/Python%20package/badge.svg)

SRT(Super Rapid Train) application python wrapper

This project was inspired from [korail2](https://github.com/carpedm20/korail2) of [carpedm20](https://github.com/carpedm20).

## Requirements

- Python >= 3.5

## Installation

```
pip install SRTrain
```

## Usage

### 1. Login

```python
>>> from SRT import SRT

>>> srt = SRT("1234567890", YOUR_PASSWORD) # with membership number
>>> srt = SRT("def6488@gmail.com", YOUR_PASSWORD) # with email
>>> srt = SRT("010-1234-xxxx", YOUR_PASSWORD) # with phone number
```

use `verbose` option to see some debugging messages

```python
srt = SRT("010-1234-xxxx", YOUR_PASSWORD, verbose=True)
```

### 2. Searching trains

use `search_train` method.

- dep : A departure station in Korean ex) '수서'
- arr : A arrival station in Korean ex) '부산'
- date : (optional) (default: today) A departure date in yyyyMMdd format 
- time : (optional) (default: 000000) A departure time in hhmmss format 
- available_only: (optional) (default: True) return trains with available seats only 

```python
>>> dep = '수서'
>>> arr = '부산'
>>> date = '20190913'
>>> time = '144000'
>>> trains = srt.search_train(dep, arr, date, time)
>>> trains
# [[SRT] 09월 30일, 수서~부산(15:00~17:34) 특실 예약가능, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(15:30~18:06) 특실 예약가능, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(16:00~18:24) 특실 매진, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(16:25~18:45) 특실 예약가능, 일반실 예약가능, ...]
```

### 3. Making a reservation

use `reserve` method.

- train: `SRTTrain` object returned by `search_train()`
- passengers (optional, default is one Adult)
```python
>>> trains = srt.search_train(dep, arr, date, time)
>>> reservation = srt.reserve(trains[0])
>>> reservation
# [SRT] 09월 30일, 수서~부산(15:30~18:06) 130700원(3석), 구입기한 09월 20일 23:38

>>> from passengers import Adult, Child
>>> srt.reserve(trains[1], passengers=[Adult(), Adult(), Child()])
```

#### Passenger class

__WARNING: 충분히 테스트되지 않음__

Highly inspired by [@dotaitch](https://github.com/dotaitch)'s [Passenger](https://github.com/dotaitch/SRTpy/blob/master/SRTpy/srt.py#L221) class

- Adult
- Child
- Senior
- Disability1To3
- Disability4To6

### 4. Getting reserved tickets

Use `get_reservations()` method.

```python
>>> reservations = srt.get_reservations()
>>> reservations
# [[SRT] 09월 30일, 수서~부산(15:30~18:06) 130700원(3석), 구입기한 09월 19일 19:11]

>>> reservations[0].tickets
# [18호차 9C (일반실) 어른/청소년 [52300원(600원 할인)],
# 18호차 10C (일반실) 어른/청소년 [52300원(600원 할인)],
# 18호차 10D (일반실) 장애 4~6급 [26100원(26800원 할인)]]
```

### 5. Canceling reservation

Use `cancel` method.

- reservation: `SRTreservation` object returned by `reserve()` or  returned by `get_reservations()`

```python
>>> reservation = srt.reserve(train)
>>> srt.cancel(reservation)

>>> reservations = srt.get_reservations()
>>> srt.cancel(reservations[0])
```

## Changelog

- 0.1.3 (2019/02/15): `search_train()` 에서 매진되지 않은 좌석만 리턴하는 옵션을 디폴트로 추가
- 0.1.5 (2019/02/15): 매진 확인 오류 수정
- 1.0.0 (2019/09/13): SRT 앱 NEO 업데이트에 맞추어 API 전체 완전 수정 (#1)

## TODO

- Add tests for CI
