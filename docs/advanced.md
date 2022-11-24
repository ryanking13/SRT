# Advanced Usages

SRT 로그인, 승차표 찾기 설명은 생략합니다.

```python
>>> from SRT import SRT, SeatType
>>> srt = SRT('your-id', 'your-password')
>>> trains = srt.search_train('수서', '대전', '20221122', '000000')
```

## 승객 여러명 예약하기

**WARNING: 충분히 테스트되지 않음**

Highly inspired by [@dotaitch](https://github.com/dotaitch).

예시) 어른 2명, 어린이 1명 예약
```python
>>> from SRT.passenger import Adult, Child
>>> srt.reserve(trains[0], passengers=[Adult(), Adult(), Child()])
```

- Adult: 어른/청소년
- Child: 어린이
- Senior: 경로
- Disability1To3: 장애 1~3급
- Disability4To6: 장애 4~6급

## 일반실 / 특실 좌석 옵션 선택하기

예시) 일반실 우선 예약
```python
>>> from SRT import SeatType
>>> srt.reserve(self, trains[0], special_seat=SeatType.GENERAL_FIRST)
```

- SeatType.GENERAL_FIRST : 일반실 우선
- SeatType.GENERAL_ONLY : 일반실만
- SeatType.SPECIAL_FIRST : 특실 우선
- SeatType.SPECIAL_ONLY : 특실만
