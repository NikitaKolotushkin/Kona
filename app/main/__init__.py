#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint


main = Blueprint('main', __name__, template_folder='templates_dir', static_folder='static_dir')


from . import views