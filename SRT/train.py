from .constants import *


class Train:
    pass


class SRTTrain(Train):
    def __init__(self, data):
        self.train_code = data["stlbTrnClsfCd"]
        self.train_name = TRAIN_NAME[self.train_code]
        self.train_number = data["trnNo"]
        self.dep_date = data["dptDt"]
        self.dep_time = data["dptTm"]
        self.dep_station_code = data["dptRsStnCd"]
        self.dep_station_name = STATION_NAME[self.dep_station_code]
        self.arr_date = data["arvDt"]
        self.arr_time = data["arvTm"]
        self.arr_station_code = data["arvRsStnCd"]
        self.arr_station_name = STATION_NAME[self.arr_station_code]
        self.general_seat_state = data["gnrmRsvPsbStr"]
        self.special_seat_state = data["sprmRsvPsbStr"]

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
            "특실 {special_state}, 일반실 {general_state}"
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
            special_state=self.special_seat_state,
            general_state=self.general_seat_state,
        )

        return d

    def general_seat_available(self):
        return "예약가능" in self.general_seat_state

    def special_seat_available(self):
        return "예약가능" in self.special_seat_state

    def seat_available(self):
        return self.general_seat_available() or self.special_seat_available()
