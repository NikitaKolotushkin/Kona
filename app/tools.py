#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def validate_email(email):
    pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    return bool(re.match(pattern, email))