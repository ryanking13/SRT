from SRT.passenger import (
    Adult,
    Child,
    Disability1To3,
    Disability4To6,
    Passenger,
    Senior,
)


def test_get_passenger_dict():
    passengers = [
        Adult(),
        Child(),
        Child(),
    ]

    passengers = Passenger.combine(passengers)

    data = Passenger.get_passenger_dict(passengers)
    assert data["totPrnb"] == "3"
    assert data["psgGridcnt"] == "2"
    assert data["psgTpCd1"] == "5"
    assert data["psgInfoPerPrnb1"] == "2"
    assert data["psgTpCd2"] == "1"
    assert data["psgInfoPerPrnb2"] == "1"

    passengers2 = [
        Senior(),
        Disability1To3(),
        Disability4To6(),
    ]

    passengers2 = Passenger.combine(passengers2)

    data = Passenger.get_passenger_dict(passengers2)
    assert data["totPrnb"] == "3"
    assert data["psgGridcnt"] == "3"
    assert data["psgTpCd1"] == "3"
    assert data["psgInfoPerPrnb1"] == "1"
    assert data["psgTpCd2"] == "2"
    assert data["psgInfoPerPrnb2"] == "1"
    assert data["psgTpCd3"] == "4"
    assert data["psgInfoPerPrnb3"] == "1"
