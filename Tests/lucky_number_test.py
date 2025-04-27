import datetime
from flask_server.website.profile.service import generateLuckyNumber  # zaimportuj funkcję z odpowiedniego modułu

def test_generate_lucky_number_range():
    # Test sprawdzający, czy liczba szczęśliwa jest w zakresie 1-20
    lucky_number = generateLuckyNumber()
    assert 1 <= lucky_number <= 20

def test_generate_lucky_number_consistency():
    # Test sprawdzający konsystencję wyniku w tym samym dniu
    lucky_number_first = generateLuckyNumber()
    lucky_number_second = generateLuckyNumber()
    assert lucky_number_first == lucky_number_second

def test_generate_lucky_number_different_days():
    # Test sprawdzający, czy liczby są różne dla różnych dni
    today = datetime.date.today()
    lucky_number_today = generateLuckyNumber(today)

    tomorrow = today + datetime.timedelta(days=2)
    lucky_number_tomorrow = generateLuckyNumber(tomorrow)

    assert lucky_number_today != lucky_number_tomorrow

