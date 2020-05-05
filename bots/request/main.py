from flask import json

from app.api.models.user import RequestUser
from bots.request.actions import *


def request_recognition(id, data):
    try:
        RequestUser.get(RequestUser.vk_id == id)
    except RequestUser.DoesNotExist:
        RequestUser.create(vk_id=id)
        send_message(id=id, message='Привет!\nПомощь Рядом в это непростое время :)\n\nВозможности 👇')
    else:
        message_handler(id, data)


def message_handler(id, data):
    if 'payload' in data.keys():
        payload = json.loads(data['payload'])
        action_recognition(id, data, payload)
    else:
        response_generator(id, data)


def action_recognition(id, data, payload):
    user = RequestUser.get(RequestUser.vk_id == id)
    if payload['action'] == 'make_request':
        if not user.isInfo:
            get_info(id, data)
        else:
            make_request(id, data)
    elif payload['action'] == 'save_elevator_option':
        save_elevator_option(id, data, payload['answer'])
    elif payload['action'] == 'confirm_data':
        confirm_data(id, data, payload['answer'])
    elif payload['action'] == 'show_popular':
        show_popular(id, data)
    elif payload['action'] == 'save_order':
        save_order(id, data)


def response_generator(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    if user.state is not None:
        eval(str(user.state) + '(id, data)')
    else:
        send_message(id=id, message='Извините, не понимаю, о чём Вы 🙁')
