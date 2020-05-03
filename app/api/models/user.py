from app.api.models import *


class User(BaseModel):
    id = AutoField(primary_key=True)
    vk_id = TextField()

    class Meta:
        db_table = 'Users'
