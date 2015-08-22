#!/usr/bin/env python3
import os
from app import create_app
from flask.ext.script import Manager, Server, Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))
server = Server(host="0.0.0.0", port=8080)
manager.add_command("runserver", server)

if __name__ == '__main__':
    manager.run()

