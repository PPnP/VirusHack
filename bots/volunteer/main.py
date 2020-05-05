from flask import json

from app.api.models.user import VolunteerUser
from bots.volunteer.actions import *


def volunteer_recognition(id, data):
    try:
        VolunteerUser.get(VolunteerUser.vk_id == id)
    except VolunteerUser.DoesNotExist:
        VolunteerUser.create(vk_id=id)
        send_message(id=id, message='Привет!\nМы рады, что Вы готовы помочь другим в это непростое время :)\n\nВозможности 👇')
    else:
        message_handler(id, data)


def message_handler(id, data):
    if 'payload' in data.keys():
        payload = json.loads(data['payload'])
        action_recognition(id, data, payload)
    else:
        response_generator(id, data)


def action_recognition(id, data, payload):
    if payload['action'] == 'take_order':
        get_info(id, data)
    elif payload['action'] == 'confirm_order':
        confirm_order(id, data, payload['answer'])


def response_generator(id, data):
    user = VolunteerUser.get(VolunteerUser.vk_id == id)
    if user.state is not None:
        eval(str(user.state) + '(id, data)')
    else:
        send_message(id=id, message='Извините, не понимаю, о чём Вы 🙁')
