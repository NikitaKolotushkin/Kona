#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import codecs
import json


def validate_email(email) -> bool:
    """ Проверяет валидность электронной почте по заданному регулярным выражением шаблону
    
    :rtype: bool
    :return: True если email прошел валидацию, иначе - False
    """
    pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    return bool(re.match(pattern, email))


def open_relations():
    with codecs.open('relations.json', 'r', 'utf_8_sig') as f:
        dict_obj = json.load(f)
    return dict_obj


def dump_relations(dict_obj):
    with codecs.open('relations.json', 'w', 'utf_8_sig') as file:
        json.dump(dict_obj, file)
