from app.api.models import *
from app.api.models.user import RequestUser


class Order(BaseModel):
    id = AutoField(primary_key=True)

    owner = ForeignKeyField(RequestUser, backref='orders')
    request = TextField(default='')

    class Meta:
        db_table = 'Orders'
