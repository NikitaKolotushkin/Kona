#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def validate_email(email) -> bool:
    """ Проверяет валидность электронной почте по заданному регулярным выражением шаблону
    
    :rtype: bool
    :return: True если email прошел валидацию, иначе - False
    """
    pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    return bool(re.match(pattern, email))
