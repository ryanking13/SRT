from SRT import SRT, SeatType

session = SRT("", "")
trains = session.search_train("수서", "부산", "20221122", "060000")
reserve = session.reserve(trains[0], special_seat=SeatType.SPECIAL_FIRST)
""
