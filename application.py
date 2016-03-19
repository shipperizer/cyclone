from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from cyclone.app import create_app


app = create_app()

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
