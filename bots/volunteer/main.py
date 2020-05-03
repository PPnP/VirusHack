from flask import json

from app.api.models.user import User
from bots.volunteer.actions import *


def volunteer_recognition(id, data):
    try:
        User.get(User.vk_id == id)
    except User.DoesNotExist:
        User.create(vk_id=id)
        send_message(id=id, message='Привет!\nЯ твой помогатор в это непростое время :)\n\nВозможности 👇')
    else:
        message_handler(id, data)


def message_handler(id, data):
    if 'payload' in data.keys():
        payload = json.loads(data['payload'])
        action_recognition(id, data, payload)
    else:
        response_generator(id, data)


def action_recognition(id, data, payload):
    if payload['action'] == 'some_action':
        pass


def response_generator(id, data):
    send_message(id=id, message='Извините, не понимаю, о чём Вы 🙁')
