import abc


class Passenger(metaclass=abc.ABCMeta):
    """Passenger class. Highly inspired by `srt.py`
    <https://github.com/dotaitch/SRTpy/blob/master/SRTpy/srt.py>`
    by `dotaitch`
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    def __init_internal__(self, name, type_code, count):
        self.name = name
        self.type_code = type_code
        self.count = count

    def __repr__(self):
        return "{} {}명".format(self.name, self.count)

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        if self.type_code == other.type_code:
            new_count = self.count + other.count
            return self.__class__(count=new_count)

    @classmethod
    def combine(cls, passengers):
        if list(filter(lambda x: not isinstance(x, Passenger), passengers)):
            raise TypeError("Passengers must be based on Passenger")

        tmp_passengers = passengers.copy()
        combined_passengers = []
        while tmp_passengers:
            passenger = tmp_passengers.pop()
            same_class = list(
                filter(lambda x: isinstance(x, passenger.__class__), tmp_passengers)
            )
            new_passenger = None
            if not same_class:
                new_passenger = passenger
            else:
                for same in same_class:
                    new_passenger = passenger + same
                    tmp_passengers.remove(same)

            if new_passenger.count > 0:
                combined_passengers.append(new_passenger)

        return combined_passengers

    @staticmethod
    def total_count(passengers):
        if list(filter(lambda x: not isinstance(x, Passenger), passengers)):
            raise TypeError("Passengers must be based on Passenger")

        total_count = 0
        for passenger in passengers:
            total_count += passenger.count

        return str(total_count)

    @staticmethod
    def get_passenger_dict(passengers, special_seat=False):
        if list(filter(lambda x: not isinstance(x, Passenger), passengers)):
            raise TypeError("Passengers must be based on Passenger")

        data = {
            "totPrnb": Passenger.total_count(passengers),
            "psgGridcnt": str(len(passengers)),
        }
        for i, passenger in enumerate(passengers):
            data["psgTpCd{}".format(i + 1)] = passenger.type_code
            data["psgInfoPerPrnb{}".format(i + 1)] = str(passenger.count)
            # seat location ('000': 기본, '012': 창측, '013': 복도측)
            # TODO: 선택 가능하게
            data["locSeatAttCd{}".format(i + 1)] = "000"
            # seat requirement ('015': 일반, '021': 휠체어)
            # TODO: 선택 가능하게
            data["rqSeatAttCd{}".format(i + 1)] = "015"
            # seat direction ('009': 정방향)
            data["dirSeatAttCd{}".format(i + 1)] = "009"

            data["smkSeatAttCd{}".format(i + 1)] = "000"
            data["etcSeatAttCd{}".format(i + 1)] = "000"
            # seat type: ('1': 일반실, '2': 특실)
            data["psrmClCd{}".format(i + 1)] = "2" if special_seat else "1"

        return data


class Adult(Passenger):
    def __init__(self, count=1):
        super().__init__()
        super().__init_internal__("어른/청소년", "1", count)


class Child(Passenger):
    def __init__(self, count=1):
        super().__init__()
        super().__init_internal__("어린이", "5", count)


class Senior(Passenger):
    def __init__(self, count=1):
        super().__init__()
        super().__init_internal__("경로", "4", count)


class Disability1To3(Passenger):
    def __init__(self, count=1):
        super().__init__()
        super().__init_internal__("장애 1~3급", "2", count)


class Disability4To6(Passenger):
    def __init__(self, count=1):
        super().__init__()
        super().__init_internal__("장애 4~6급", "3", count)
