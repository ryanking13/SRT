from constants import *


class SRTReservation:

    def __init__(self, ticket, data):
        self.reservation_number = ticket['pnrNo']
        self.total_cost = ticket['rcvdAmt']
        self.seat_count = ticket['tkSpecNum']

        self.train_code = data['stlbTrnClsfCd']
        self.train_name = TRAIN_NAME[self.train_code]
        self.train_number = data['trnNo']
        self.dep_date = data['dptDt']
        self.dep_time = data['dptTm']
        self.dep_station_code = data['dptRsStnCd']
        self.dep_station_name = STATION_NAME[self.dep_station_code]
        self.arr_time = data['arvTm']
        self.arr_station_code = data['arvRsStnCd']
        self.arr_station_name = STATION_NAME[self.arr_station_code]
        self.payment_date = data['iseLmtDt']
        self.payment_time = data['iseLmtTm']

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def dump(self):
        d = (
            '[{name}] '
            '{month}월 {day}일, '
            '{dep}~{arr}'
            '({dep_hour}:{dep_min}~{arr_hour}:{arr_min}) '
            '{cost}원({seats}석), '
            '구입기한 {pay_month}월 {pay_day}일 {pay_hour}:{pay_min}'
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