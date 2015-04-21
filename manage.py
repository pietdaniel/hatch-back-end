#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

import os

from neuhatch import app, db
from neuhatch.models import *

"""
This module contains our flask-script functionality.
You can run this script with no arguments to get a list of functionality.
"""


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Executes our test suite."""
    import nose
    nose.main(argv=[''])


if __name__ == '__main__':
    manager.run()
