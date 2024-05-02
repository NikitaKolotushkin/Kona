#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_script import Manager, Shell

from app import create_app, db
from app.models import User, University
from config import current_config
from manager_commands import Runner

app, sio = create_app(config_class=current_config)
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, University=University, sio=sio)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('run_app', Runner(app))

if __name__ == '__main__':
    manager.run()
    sio.run(app)
