from app.api.models import *


class User(BaseModel):
    id = AutoField(primary_key=True)
    vk_id = TextField()

    name = TextField(null=True, default=None)
    phone = TextField(null=True, default=None)

    city = TextField(null=True, default=None)
    street = TextField(null=True, default=None)
    building = TextField(null=True, default=None)
    apartment = TextField(null=True, default=None)
    floor = TextField(null=True, default=None)
    isElevator = BooleanField(default=False)

    isInfo = BooleanField(default=False)
    state = TextField(default='default')

    class Meta:
        db_table = 'Users'
