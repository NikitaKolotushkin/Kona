# Kona

![Основной постер](/app/static/img/kona_poster_1.png)

Приложение для поиска компаньонов с целью участия в стартапах / проектах / грантовых мероприятиях

# Установка

**Рекомендуется использовать Unix-подобные ОС (Linux, MacOS)**

+ ``` git clone http://github.com/NikitaKolotushkin/Kona.git ```
+ ``` cd Kona/ ```
+ ``` pip install virtualenv ```
+ ``` virtualenv venv ```
+ ``` source venv/bin/activate ```
+ ``` pip install -r requirements.txt ```
+ ``` flask db init ```
+ ``` flask db migrate ```
+ ``` flask db upgrade ```
+ ``` python3 runner.py run_app ```

# TODO:

+ Создать анкету пользователя 
+ Система друзей
+ Возможность добавлять мероприятия