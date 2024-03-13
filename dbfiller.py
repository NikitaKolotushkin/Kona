#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import json

from app import db, engine
from app.models import *


def fill_cities() -> None:
    with codecs.open('cities.json', 'r', 'utf_8_sig') as f:
        data = [city for city in json.loads(f.read()).keys()]
    return data


def fill_universities() -> None:
    with codecs.open('cities.json', 'r', 'utf_8_sig') as f:
        data = sum([university for university in json.loads(f.read()).values() if university[0] != ''], [])
    return data


def fill_interests() -> None:
    return


def main():
    print(fill_universities())


if __name__ == '__main__':
    main()