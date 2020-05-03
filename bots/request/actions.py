import random
import string

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from bots.request import vk


def get_default_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Кнопка 1', color=VkKeyboardColor.PRIMARY, payload={'action': 'some_action'})
    keyboard.add_line()
    keyboard.add_button(label='Кнопка 2', color=VkKeyboardColor.DEFAULT, payload={'action': 'some_action'})
    default_keyboard = keyboard.get_keyboard()
    return default_keyboard


def send_message(id, message, attachment='', keyboard=get_default_keyboard()):
    random_id = int(''.join(random.choice(string.digits) for _ in range(10)))
    vk.messages.send(user_id=id, random_id=random_id, message=message, attachment=attachment, keyboard=keyboard)
