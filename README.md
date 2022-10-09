# SRT

![github actions badge](https://github.com/ryanking13/SRT/workflows/Python%20package/badge.svg)
[![Downloads](https://pepy.tech/badge/srtrain)](https://pepy.tech/project/srtrain)
[![Downloads](https://pepy.tech/badge/srtrain/month)](https://pepy.tech/project/srtrain)
[![Documentation Status](https://readthedocs.org/projects/srtrain/badge/?version=latest)](https://srtrain.readthedocs.io/en/latest/?badge=latest)


SRT(Super Rapid Train) application python wrapper

With `SRTrain`, you **can**:

- Search SRT train schedules.
- Reserve SRT trains.
- Find your reservations/tickets information.
- Cancel reservations/tickets.

while you **can't**:

- Pay for a ticket.
- Search or reserve non-SRT trains (KTX, ITX, ... ) (use [korail2](https://github.com/carpedm20/korail2) instead)

This project was inspired from [korail2](https://github.com/carpedm20/korail2) of [carpedm20](https://github.com/carpedm20).

## Quickstart

```
pip install SRTrain
```

```python
>>> from SRT import SRT
>>> srt = SRT("010-1234-xxxx", YOUR_PASSWORD)

>>> dep = '수서'
>>> arr = '부산'
>>> date = '20190930'
>>> time = '144000'
>>> trains = srt.search_train(dep, arr, date, time)
>>> trains
# [[SRT] 09월 30일, 수서~부산(15:00~17:34) 특실 예약가능, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(15:30~18:06) 특실 예약가능, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(16:00~18:24) 특실 매진, 일반실 예약가능,
# [SRT] 09월 30일, 수서~부산(16:25~18:45) 특실 예약가능, 일반실 예약가능, ...]

>>> reservation = srt.reserve(trains[1])
>>> reservation
# [SRT] 09월 30일, 수서~부산(15:30~18:06) 53700원(1석), 구입기한 09월 20일 23:38
```

## Documentation

See [documentation](https://srtrain.readthedocs.io/en/latest/).

## See Also

- [go-SRT](https://github.com/ryanking13/go-SRT): SRT golang wrapper
