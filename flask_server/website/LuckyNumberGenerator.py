import random
import datetime


# generating lucky number that stays the same during the day and changes the next day

def generateLuckyNumber(current_date=None):
    if current_date is None:
        current_date = datetime.date.today()
    seed_date = current_date.toordinal()
    random.seed(seed_date)
    lucky_number = random.randint(1, 20)
    return lucky_number
