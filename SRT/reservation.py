from .constants import STATION_NAME, TRAIN_NAME


class SRTTicket:
    SEAT_TYPE = {"1": "일반실", "2": "특실"}

    PASSENGER_TYPE = {
        "1": "어른/청소년",
        "2": "장애 1~3급",
        "3": "장애 4~6급",
        "4": "경로",
        "5": "어린이",
    }

    def __init__(self, data):
        self.car = data["scarNo"]
        self.seat = data["seatNo"]
        self.seat_type_code = data["psrmClCd"]
        self.seat_type = self.SEAT_TYPE[self.seat_type_code]
        self.passenger_type_code = data["psgTpCd"]
        self.passenger_type = self.PASSENGER_TYPE[self.passenger_type_code]

        self.price = int(data["rcvdAmt"])
        self.original_price = int(data["stdrPrc"])
        self.discount = int(data["dcntPrc"])

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def dump(self):
        d = (
            f"{self.car}호차 {self.seat} ({self.seat_type}) {self.passenger_type} "
            f"[{self.price}원({self.discount}원 할인)]"
        )

        return d


class SRTReservation:
    def __init__(self, train, pay, tickets):
        self.reservation_number = train["pnrNo"]
        self.total_cost = train["rcvdAmt"]
        self.seat_count = train["tkSpecNum"]

        self.train_code = pay["stlbTrnClsfCd"]
        self.train_name = TRAIN_NAME.get(
            self.train_code, "알 수 없는 열차 코드 (업데이트 필요)"
        )
        self.train_number = pay["trnNo"]
        self.dep_date = pay["dptDt"]
        self.dep_time = pay["dptTm"]
        self.dep_station_code = pay["dptRsStnCd"]
        self.dep_station_name = STATION_NAME.get(
            self.dep_station_code, "알 수 없는 역 코드 (업데이트 필요)"
        )
        self.arr_time = pay["arvTm"]
        self.arr_station_code = pay["arvRsStnCd"]
        self.arr_station_name = STATION_NAME.get(
            self.arr_station_code, "알 수 없는 역 코드 (업데이트 필요)"
        )
        self.payment_date = pay["iseLmtDt"]
        self.payment_time = pay["iseLmtTm"]

        self.paid = pay["stlFlg"] == "Y"  # 결제 여부
        self._tickets = tickets

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def dump(self):
        d = (
            f"[{self.train_name}] "
            f"{self.dep_date[4:6]}월 {self.dep_date[6:8]}일, "
            f"{self.dep_station_name}~{self.arr_station_name}"
            f"({self.dep_time[0:2]}:{self.dep_time[2:4]}~{self.arr_time[0:2]}:{self.arr_time[2:4]}) "
            f"{self.total_cost}원({self.seat_count}석)"
        )
        if not self.paid:
            d += f", 구입기한 {self.payment_date[4:6]}월 {self.payment_date[6:8]}일 {self.payment_time[0:2]}:{self.payment_time[2:4]}"
        return d

    @property
    def tickets(self):
        return self._tickets
