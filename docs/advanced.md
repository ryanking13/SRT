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

## 결제하기

**⚠️ 주의: 이 API는 실제로 결제를 수행합니다**<br>
해당 결제 API는 비공식적인 API를 사용하기 때문에 언제든지 제대로 동작하지 않을 수 있습니다.<br>
이에 따른 문제 발생에 대한 책임은 API 사용자 본인에게 있음을 알립니다.<br>

---

```python
>>> reservation = srt.reserve(trains[0])
>>> srt.pay_with_card(
        reservation,
        number="1234567890123456",
        password="12",
        validation_number="981204",
        expire_date="2309",
    )
```

### 각 파라미터 기입요령

| 순서 | 변수명            | 설명                                                                                                                   | 예시                 | 기본 값 |
| ---- | ----------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------- | ------- |
| 1    | reservation       | **결제대상 예약내역**                                                                                                  | -                    | -       |
| 2    | number            | **결제 카드번호** <br>_\* 하이픈(-) 제외_                                                                              | `"1234000056780000"` | -       |
| 3    | password          | **카드비밀번호 앞 2자리**                                                                                              | `"12"`               | -       |
| 4    | validation_number | **개인(`J`)인 경우: 생년월일<br>법인(`S`)인 경우: 사업자번호**                                                         | `"981204"`           | -       |
| 5    | expire_date       | **카드유효기간** <br>_\* YYMM(연도+월) 형식의 만료일을 입력<br>\*카드 표현방식 MMYY(월+연도)형식과 착오에 주의_        | `"2309"`             | -       |
| 6    | installment       | **할부선택** <br>_\* 할부 개월 수 입력, 0의 경우 일시불.<br> \* 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24 개월 선택 가능_ | `0`                  | `0`     |
| 7    | card_type         | **카드 유형** <br>_\* J : 개인, S : 법인_                                                                              | `"J"`                | `"J"`   |

## 여러 SRT 간, netFunnelKey 공유하기

> 열차 검색 (`search_train`)시, 트래픽을 제어하기 위해 netfunnel 이 사용되고 있습니다.
> 열차를 검색하기 전, `netFunnelKey` 를 발급받아 이를 함께 전달하게 되는데, 사용량이 많을때에는 `netFunnelKey` 발급에 오랜 시간이 걸릴 수 있습니다.
> 이를 조금이라도 해소하기 위해 본 라이브러리에서는 발급된 `netFunnelKey`를 내부적으로 저장(캐싱)하고, 만료(발급 후 약 50초)까지 사용될 수 있게 하여 `netFunnelKey`발급에 소요되는 시간을 단축하고 있습니다.

`SRT`객체를 여러개 생성해서 사용하는 경우, 인스턴스 생성 시 `NetFunnelHelper`를 주입하여 `SRT`간 `netFunnelKey`를 공유하도록 처리할 수 있습니다.

### 예시

```python
# netFunnelKey를 내부적으로 관리하는 netfunnel_helper를 생성합니다.
netfunnel_helper = NetFunnelHelper()

# 첫번 째 SRT객체 생성 시 netfunnel_helper를 주입합니다.
srt1 = SRT(
    # ...
    netfunnel_helper=netfunnel_helper
)

# 두번 째 SRT객체 생성 시 netfunnel_helper를 주입합니다.
srt2 = SRT(
    # ...
    netfunnel_helper=netfunnel_helper
)

# 위와같은 처리를 통해

# 처음 요청한 이곳에서 발급된 `netFunnelKey`를
srt1.search_train(
    # ...
)

# 두번 째 요청한 이곳에서도 함께 공유할 수 있게 되었습니다.
srt2.search_train(
    # ...
)

```
