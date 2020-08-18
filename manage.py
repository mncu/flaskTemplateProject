from flask_script import Manager, Server
from flask_migrate import MigrateCommand, Migrate
from xyzFfootball.app import app
from xyzFfootball.orm import *

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
