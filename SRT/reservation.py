from .constants import *


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
            "{car}호차 {seat} ({seat_type}) {passenger_type} "
            "[{price}원({discount}원 할인)]"
        ).format(
            car=self.car,
            seat=self.seat,
            seat_type=self.seat_type,
            passenger_type=self.passenger_type,
            price=self.price,
            discount=self.discount,
        )

        return d


class SRTReservation:
    def __init__(self, train, pay, tickets):
        self.reservation_number = train["pnrNo"]
        self.total_cost = train["rcvdAmt"]
        self.seat_count = train["tkSpecNum"]

        self.train_code = pay["stlbTrnClsfCd"]
        self.train_name = TRAIN_NAME[self.train_code]
        self.train_number = pay["trnNo"]
        self.dep_date = pay["dptDt"]
        self.dep_time = pay["dptTm"]
        self.dep_station_code = pay["dptRsStnCd"]
        self.dep_station_name = STATION_NAME[self.dep_station_code]
        self.arr_time = pay["arvTm"]
        self.arr_station_code = pay["arvRsStnCd"]
        self.arr_station_name = STATION_NAME[self.arr_station_code]
        self.payment_date = pay["iseLmtDt"]
        self.payment_time = pay["iseLmtTm"]

        self._tickets = tickets

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def dump(self):
        d = (
            "[{name}] "
            "{month}월 {day}일, "
            "{dep}~{arr}"
            "({dep_hour}:{dep_min}~{arr_hour}:{arr_min}) "
            "{cost}원({seats}석), "
            "구입기한 {pay_month}월 {pay_day}일 {pay_hour}:{pay_min}"
        ).format(
            name=self.train_name,
            month=self.dep_date[4:6],
            day=self.dep_date[6:8],
            dep=self.dep_station_name,
            arr=self.arr_station_name,
            dep_hour=self.dep_time[0:2],
            dep_min=self.dep_time[2:4],
            arr_hour=self.arr_time[0:2],
            arr_min=self.arr_time[2:4],
            cost=self.total_cost,
            seats=self.seat_count,
            pay_month=self.payment_date[4:6],
            pay_day=self.payment_date[6:8],
            pay_hour=self.payment_time[0:2],
            pay_min=self.payment_time[2:4],
        )

        return d

    @property
    def tickets(self):
        return self._tickets
