|Method|Endpoint|Requied data|Returned data|
|------|--------|------------|-------------|
|?POST?|login|username, password|status zalogowania, user_ID|
|POST|adding a new user|typ_użytkownika, typ_nowego_użytkownika, name, surname, photo, class, email, phone number, data urodzenia, miejsce zamieszkania|czy istnieje, user_id|
|GET|wyszukiwarka|string|user_id, name, surname|
|GET|your_profile|user_id|name, surname, photo, class, main teacher, student number, email, phone number|
|GET|teacher's profile|user_type, teacher_id|name, surname, photo, description, email, phone number, room|
|GET|parent's profile|user_type, parent_id|name, surname, photo, class, main teacher, email, phone number|
|GET|student's profile|user_type, student_id|name, surname, photo, class, main teacher, student number, email, phone number|
|POST|adding a grade|user_type, name, surname, class, lesson|grade, weight, date, description|
|GET|grades|student_id|nazwa_przedmiotu, grades, average|
|GET|ranking|...|...|
|GET|plan zajęć|id_klasy|id_zajec, id_przedmiotu, id_ nauczyciela, dzień_tygodnia, godzina_rozpoczęcia, godzina_zakończenia, budynek, sprawdzian|
|POST|dodaj sprawdzian|id_zajęć, opis, user_type|opis|
|POST|dodaj ogłoszenie|user_type, tytuł, wpis|wpis, data|
|GET|ogłoszenie|user_type|opis ogłoszenia, data ogłoszenia|
|POST|archiwum ogłoszeń|data, id_ogłoszenia|w_archiwum=1|
