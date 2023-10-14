CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    user_login CHAR (64) NOT NULL UNIQUE, 
    user_email CHAR (64) NOT NULL UNIQUE,
    user_tag CHAR (64) NOT NULL UNIQUE,
    user_password_hash VARCHAR (256) NOT NULL,
    user_name VARCHAR (64) NOT NULL,
    user_surname VARCHAR (64) NOT NULL,
    user_phone CHAR (32),
    user_description VARCHAR (2048),
    user_photo VARBINARY (8000),
    user_city VARCHAR (64),
    user_university VARCHAR (256)
);

CREATE TABLE IF NOT EXISTS Universities (
    university_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE
);