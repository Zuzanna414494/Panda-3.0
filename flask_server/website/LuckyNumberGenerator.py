import random
import datetime


# generating lucky number that stays the same during the day and changes the next day

def generateLuckyNumber():
    current_date = datetime.date.today().toordinal()

    random.seed(current_date)

    lucky_number = random.randint(1, 20)
    return lucky_number
