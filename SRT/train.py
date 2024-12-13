from .constants import STATION_NAME, TRAIN_NAME


class Train:
    pass


class SRTTrain(Train):
    def __init__(self, data):
        self.train_code = data["stlbTrnClsfCd"]
        self.train_name = TRAIN_NAME.get(
            self.train_code, "알 수 없는 열차 코드 (업데이트 필요)"
        )
        self.train_number = data["trnNo"]
        self.dep_date = data["dptDt"]
        self.dep_time = data["dptTm"]
        self.dep_station_code = data["dptRsStnCd"]
        self.dep_station_name = STATION_NAME.get(
            self.dep_station_code, "알 수 없는 역 코드 (업데이트 필요)"
        )
        self.arr_date = data["arvDt"]
        self.arr_time = data["arvTm"]
        self.arr_station_code = data["arvRsStnCd"]
        self.arr_station_name = STATION_NAME.get(
            self.arr_station_code, "알 수 없는 역 코드 (업데이트 필요)"
        )
        self.general_seat_state = data["gnrmRsvPsbStr"]
        self.special_seat_state = data["sprmRsvPsbStr"]
        self.reserve_wait_possible_code = data["rsvWaitPsbCd"]
        self.arr_station_run_order = data["arvStnRunOrdr"]
        self.arr_station_constitution_order = data["arvStnConsOrdr"]
        self.arr_station_constitution_order = data["arvStnConsOrdr"]
        self.dep_station_run_order = data["dptStnRunOrdr"]
        self.dep_station_constitution_order = data["dptStnConsOrdr"]

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def dump(self):
        d = (
            "[{name} {number}] "
            "{month}월 {day}일, "
            "{dep}~{arr}"
            "({dep_hour}:{dep_min}~{arr_hour}:{arr_min}) "
            "특실 {special_state}, 일반실 {general_state}, 예약대기 {reserve_standby_state}"
        ).format(
            name=self.train_name,
            number=self.train_number,
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
            reserve_standby_state=(
                "가능" if self.reserve_standby_available() else "불가능"
            ),
        )

        return d

    def general_seat_available(self):
        return "예약가능" in self.general_seat_state

    def special_seat_available(self):
        return "예약가능" in self.special_seat_state

    def reserve_standby_available(self):
        return (
            "9" in self.reserve_wait_possible_code
        )  # 9인 경우, 예약대기 가능한 상태임

    def seat_available(self):
        return self.general_seat_available() or self.special_seat_available()
