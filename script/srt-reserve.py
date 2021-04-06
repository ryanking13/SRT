from SRT import SRT
from rich import print
from rich.prompt import Prompt
from PyInquirer import prompt as prompt_choice

SRT_STATIONS = (
    "수서",
    "동탄",
    "지제",
    "천안아산",
    "오송",
    "대전",
    "공주",
    "익산",
    "정읍",
    "광주송정",
    "나주",
    "목포",
    "김천구미",
    "동대구",
    "신경주",
    "울산(통도사)",
    "부산",
)


def hi():
    print("""
░██████╗██████╗░████████╗
██╔════╝██╔══██╗╚══██╔══╝
╚█████╗░██████╔╝░░░██║░░░
░╚═══██╗██╔══██╗░░░██║░░░
██████╔╝██║░░██║░░░██║░░░
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░
""")


def login():
    username = ""
    password = ""

    while not username:
        username = Prompt.ask("[bold magenta]Username")
    
    while not password:
        password = Prompt.ask("[bold magenta]Password", password=True)

    return SRT(username, password)


def select_train(client):
    station_dep = ""
    station_arr = ""
    date_dep = ""

    questions = [
        {
            "type": "list",
            "name": "station_dep",
            "message": "출발역",
            "choices": SRT_STATIONS,
        },
        {
            "type": "list",
            "name": "station_arr",
            "message": "도착역",
            "choices": SRT_STATIONS,
        },
        {
            "type": "list",
            "name": "station_arr",
            "message": "도착역",
            "choices": SRT_STATIONS,
        },
    ]

    station_dep = prompt_choice(questions)["station_dep"]
    print(answers)

	# // Step 3) Select Date

	# nextCnt := 0
	# numDays := 10
	# toPrev := "이전 날짜로"
	# toNext := "다음 날짜로"
	# for {
	# 	isNext := nextCnt > 0
	# 	days := make([]string, 0)

	# 	if isNext {
	# 		days = append(days, toPrev)
	# 	}

	# 	date := today().NextDay(nextCnt * numDays)
	# 	for i := 0; i < numDays; i++ {
	# 		days = append(days, date.String())
	# 		date = date.NextDay(1)
	# 	}
	# 	days = append(days, toNext)

	# 	err = survey.AskOne(
	# 		&survey.Select{
	# 			Message: "날짜:",
	# 			Options: days,
	# 			Default: days[0],
	# 		},
	# 		&dateDep,
	# 	)

	# 	if err != nil {
	# 		return nil, err
	# 	}

	# 	if dateDep == toPrev {
	# 		nextCnt--
	# 		continue
	# 	} else if dateDep == toNext {
	# 		nextCnt++
	# 		continue
	# 	}
	# 	break
	# }

	# if err != nil {
	# 	return nil, err
	# }

	# return &srt.SearchParams{
	# 	Dep:  stationDep,
	# 	Arr:  stationArr,
	# 	Date: dateDep,
	# }, nil


def search_train(client, params):
    pass


def reserve(client, params):
    pass


def main():
    hi()
    srt = login()

    select_train(srt)



if __name__ == "__main__":
    main()