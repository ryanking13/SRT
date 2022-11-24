from enum import Enum


class SeatType(Enum):
    GENERAL_FIRST = 1  # 일반실 우선
    GENERAL_ONLY = 2  # 일반실만
    SPECIAL_FIRST = 3  # 특실 우선
    SPECIAL_ONLY = 4  # 특실만
