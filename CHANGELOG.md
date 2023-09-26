## Unreleased

## v2.3.0 (2023/09/26)

- 카드 결제 기능 추가
  ([#249](https://github.com/ryanking13/SRT/pull/249))

## v2.2.0 (2023/08/22)

- 예약 대기 기능 추가
  ([#247](https://github.com/ryanking13/SRT/pull/247))

## v2.1.0 (2023/08/15)

- [SRT 열차운행 조정 알림](https://etk.srail.kr/cms/article/view.do?postNo=554&pageId=TK0502000000)에 따른 신규 정차역 코드 및 이름 추가.
  ([#243](https://github.com/ryanking13/SRT/pull/243))

## v2.0.8 (2023/08/02)

- `search_train()` 메소드가 더이상 사용자의 로그인 여부를 확인하지 않음.
  ([#238](https://github.com/ryanking13/SRT/pull/238))

- Public API에 대한 static typing 추가
  ([#234](https://github.com/ryanking13/SRT/pull/234))

## v2.0.7 (2023/04/05)

- get_reservations() 메소드에 결제된 예약 내역만 반환하도록 하는 payed_only 옵션 추가
  ([#228](https://github.com/ryanking13/SRT/pull/228))

## v2.0.6 (2023/02/23)

- 지제역 이름 변경 반영 ([#221](https://github.com/ryanking13/SRT/pull/221))

## v2.0.5 (2022/11/24)

- SRT 좌석 유형 옵션 기능 추가 ([#201](https://github.com/ryanking13/SRT/pull/201))

## v2.0.4 (2022/10/31)

- SRT 중복 예약 오류 반환 로직 제거 ([#193](https://github.com/ryanking13/SRT/pull/193))

## v2.0.3 (2022/06/11)

- search_train() 함수에 time_limit parameter 추가 ([#130](https://github.com/ryanking13/SRT/pull/130))
- 서대구 코드 추가 ([#166](https://github.com/ryanking13/SRT/pull/166))

## v2.0.2 (2021/06/28)

- 공식 문서 추가
- PEP517(pyproject.toml) 적용
- PyPI 릴리즈 자동화

## v2.0.1 (2021/04/07)

- SRT 이외의 열차 검색 결과에 나타나지 않도록 필터링
- `srt-reserve` 스크립트 추가

## v2.0.0 (2021/01/22)

- 업데이트된 SRT API URL 반영
- 열차 검색, 예약, 취소 테스트 추가

## v1.0.2 (2019/12/24)

- 기본 로그인/로그아웃 테스트 추가
- CI 도구 CircleCI에서 Github Actions로 교체

## v1.0.0 (2019/09/13)

- SRT 앱 NEO 업데이트에 맞추어 API 전체 완전 수정 (#1)

## v0.1.5 (2019/02/15)

- 매진 확인 오류 수정

## v0.1.3 (2019/02/15)

- `search_train()` 에서 매진되지 않은 좌석만 리턴하는 옵션을 디폴트로 추가
