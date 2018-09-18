# SRT

### __UNDER DEVELOPMENT__

SR python wrapper

This project was inspired from [korail2](https://github.com/carpedm20/korail2) of [carpedm20](https://github.com/carpedm20).

### How to Use

```python3
# git clone https://github.com/ryanking13/SRT
from srt import SRT

srt = SRT('your_id', 'your_password')
trains = srt.search_train(dep='수서', arr='부산', date='20180928', time='000000')
# [[SRT] 09월 24일, 수서~부산(09:05~11:41) 특실 예약가능, 일반실 예약가능, ...]
srt.reserve(trains[0])
```

### Features

- login
- search
- reserve

## TODO

- show reservation
- cancel reservation