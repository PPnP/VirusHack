from app import app, manager
from app.api.routes import api
from app.api.models import db
from app.api.models.user import User


@manager.command
def runserver():
    app.register_blueprint(api, url_prefix='/')
    app.run(host='localhost', port=5000, debug=True)


@manager.command
def migrate():
    tables = [User]
    db.drop_tables(tables)
    db.create_tables(tables)


if __name__ == '__main__':
    manager.run()
