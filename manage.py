from app import app, manager
from app.api.routes import api
from app.api.models import db
from app.api.models.user import RequestUser, VolunteerUser
from app.api.models.order import Order


@manager.command
def runserver():
    app.register_blueprint(api, url_prefix='/')
    app.run(host='localhost', port=5000, debug=True)


@manager.command
def migrate():
    tables = [RequestUser, VolunteerUser, Order]
    db.drop_tables(tables)
    db.create_tables(tables)


if __name__ == '__main__':
    manager.run()
