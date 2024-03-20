#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import json
import sqlite3


class dbfiller:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('app/databases/dev.db')
        self.cursor = self.connection.cursor()

    
    def commit_changes(self) -> None:
        self.connection.commit()
        self.connection.close()


    def fill_cities(self) -> None:
        with codecs.open('cities.json', 'r', 'utf_8_sig') as f:
            data = [city for city in json.loads(f.read()).keys()]

        for city in data:
            self.cursor.execute('INSERT OR IGNORE INTO cities (name) VALUES (?)', (city, ))

        self.commit_changes()


    def fill_universities(self) -> None:
        with codecs.open('cities.json', 'r', 'utf_8_sig') as f:
            data = sum([university for university in json.loads(f.read()).values() if university[0] != ''], [])

        for university in data:
            pass

        self.commit_changes()


    def fill_interests(self) -> None:
        return


def main():
    filler = dbfiller()
    filler.fill_cities()
    # filler.fill_universities()
    # filler.fill_interests()


if __name__ == '__main__':
    main()
