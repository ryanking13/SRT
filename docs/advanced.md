# Advanced Usages

## 승객 여러명 예약하기

**WARNING: 충분히 테스트되지 않음**

Highly inspired by [@dotaitch](https://github.com/dotaitch).

```python
>>> from SRT.passenger import Adult, Child
>>> srt.reserve(trains[1], passengers=[Adult(), Adult(), Child()])
```

- Adult: 어른/청소년
- Child: 어린이
- Senior: 경로
- Disability1To3: 장애 1~3급
- Disability4To6: 장애 4~6급
