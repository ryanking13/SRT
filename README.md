# SRT

SRT(Super Rapid Train) application python wrapper

This project was inspired from [korail2](https://github.com/carpedm20/korail2) of [carpedm20](https://github.com/carpedm20).

## Requirements

- Python >= 3.2

## Installation

```sh
$ git clone https://github.com/ryanking13/SRT
$ pip install -r requirements.txt
```

## Usage

### 1. Login

```python
>>> from srt import SRT

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
- date : (optional) A departure date in yyyyMMdd format
- time : (optional) A departure time in hhmmss format

```python
>>> dep = '수서'
>>> arr = '부산'
>>> date = '20180930'
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

Highly inspired by [@dotaitch](https://github.com/dotaitch)'s [Passenger](https://github.com/dotaitch/SRTpy/blob/master/SRTpy/srt.py#L221) class

- Adult
- Child
- Senior
- Disability1To3
- Disability4To6

### 4. Getting reserved tickets

Use `get_tickets()` method.

```python
>>> tickets = srt.get_tickets()
>>> tickets
# [[SRT] 09월 30일, 수서~부산(15:30~18:06) 130700원(3석), 구입기한 09월 19일 19:11]
```

### 5. Reservation cancel

Use `cancel` method.

- reservation: `SRTreservation` object returned by `reserve()` or  returned by `get_tickets()`

```python
>>> reservation = srt.reserve(train)
>>> srt.cancel(reservation)

>>> tickets = srt.get_tickets()
>>> srt.cancel(tickets[0])
```

## TODO

- Reservation passenger 별 상세 정보 저장
- CI
- PyPI
