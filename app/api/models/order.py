from app.api.models import *
from app.api.models.user import User


class Order(BaseModel):
    id = AutoField(primary_key=True)

    owner = ForeignKeyField(User, backref='orders')
    request = TextField(default='')

    class Meta:
        db_table = 'Orders'
