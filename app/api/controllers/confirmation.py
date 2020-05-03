from flask.views import MethodView
from flask import request, json

from config import volunteer_confirmation_token, request_confirmation_token
from bots.volunteer.main import volunteer_recognition
from bots.request.main import request_recognition


class VolunteerConfirmationController(MethodView):
    def post(self):
        data = json.loads(request.data)
        if 'type' not in data.keys():
            return 'not vk'
        if data['type'] == 'confirmation':
            return volunteer_confirmation_token
        elif data['type'] == 'message_new':
            user_id = data['object']['message']['from_id']
            volunteer_recognition(str(user_id), data['object']['message'])
        return 'ok'



class RequestConfirmationController(MethodView):
    def post(self):
        data = json.loads(request.data)
        if 'type' not in data.keys():
            return 'not vk'
        if data['type'] == 'confirmation':
            return request_confirmation_token
        elif data['type'] == 'message_new':
            user_id = data['object']['message']['from_id']
            request_recognition(str(user_id), data['object']['message'])
        return 'ok'
