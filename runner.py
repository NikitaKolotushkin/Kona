#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_script import Command, Manager, Shell

from app import create_app, db
from config import current_config
from manager_commands import Runner


app = create_app(config_class=current_config)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('run_app', Runner(app))

if __name__ == '__main__':
    manager.run()