import random
import os
from datetime import datetime, timedelta


class Utils:
    def __init__(self, project_path='C:\\Users\\bzielinski\\PycharmProjects\\Panda-3.0'):
        self.project_path = project_path
        self.data_file_path = os.path.join(project_path, 'data_ostatniego_losowania.txt')
        self.numerek_file_path = os.path.join(project_path, 'szczesliwy_numerek.txt')

    def losuj_i_zapisz_numer(self):
        # Sprawdź datę ostatniego losowania zapisaną w pliku
        try:
            with open(self.data_file_path, 'r') as file:
                last_draw_date = datetime.strptime(file.read(), '%Y-%m-%d')
        except FileNotFoundError:
            # Jeśli plik nie istnieje, losuj numer, zapisz go i zapisz aktualną datę
            losowy_numer = random.randint(1, 30)
            with open(self.data_file_path, 'w') as file:
                file.write(datetime.now().strftime("%Y-%m-%d"))
            with open(self.numerek_file_path, 'w') as numerek_file:
                numerek_file.write(str(losowy_numer))
            return losowy_numer

        # Sprawdź, czy minęło już 1 dzień od ostatniego losowania
        dzis = datetime.now()
        if dzis - last_draw_date >= timedelta(days=1):
            losowy_numer = random.randint(1, 30)
            with open(self.data_file_path, 'w') as file:
                file.write(dzis.strftime("%Y-%m-%d"))
            with open(self.numerek_file_path, 'w') as numerek_file:
                numerek_file.write(str(losowy_numer))
            return losowy_numer
        else:
            return "Dziś już było losowanie. Spróbuj jutro."

    def odczytaj_szczesliwy_numer(self):
        try:
            with open(self.numerek_file_path, 'r') as numerek_file:
                szczesliwy_numer = int(numerek_file.readline().strip())
            return szczesliwy_numer
        except FileNotFoundError:
            return "Brak szczęśliwego numeru. Proszę przeprowadzić losowanie."
