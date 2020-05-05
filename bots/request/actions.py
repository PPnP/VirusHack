import random
import string
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from bots.request import vk
from app.api.models.user import RequestUser
from app.api.models.order import Order


def get_default_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Подать заявку', color=VkKeyboardColor.PRIMARY, payload={'action': 'make_request'})
    keyboard.add_button(label='Срочная помощь', color=VkKeyboardColor.NEGATIVE, payload={'action': 'help'})
    default_keyboard = keyboard.get_keyboard()
    return default_keyboard


def send_message(id, message, attachment='', keyboard=get_default_keyboard()):
    random_id = int(''.join(random.choice(string.digits) for _ in range(10)))
    vk.messages.send(user_id=id, random_id=random_id, message=message, attachment=attachment, keyboard=keyboard)


def get_info(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.state = 'save_name'
    user.save()
    send_message(id, 'Введите Ваше имя')


def save_name(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.name = data['text']
    user.state = 'save_phone'
    user.save()
    send_message(id, 'Введите Ваш номер телефона')


def save_phone(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.phone = data['text']
    user.state = 'save_city'
    user.save()
    send_message(id, 'Введите Ваш город проживания')


def save_city(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.city = data['text']
    user.state = 'save_street'
    user.save()
    send_message(id, 'Введите улицу')


def save_street(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.street = data['text']
    user.state = 'save_building'
    user.save()
    send_message(id, 'Введите номер дома')


def save_building(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.building = data['text']
    user.state = 'save_apartment'
    user.save()
    send_message(id, 'Введите номер квартиры')


def save_apartment(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.apartment = data['text']
    user.state = 'save_floor'
    user.save()
    send_message(id, 'Введите номер этажа')


def save_floor(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.floor = data['text']
    user.state = 'save_elevator_option'
    user.save()
    kb = VkKeyboard(one_time=True)
    kb.add_button(label='Да', color=VkKeyboardColor.POSITIVE, payload={'action': 'save_elevator_option', 'answer': True})
    kb.add_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload={'action': 'save_elevator_option', 'answer': False})
    keyboard = kb.get_keyboard()
    send_message(id, 'Есть ли в Вашем доме лифт?', keyboard=keyboard)


def save_elevator_option(id, data, option):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.isElevator = option
    user.state = 'default'
    user.save()
    kb = VkKeyboard(one_time=True)
    kb.add_button(label='Данные верны', color=VkKeyboardColor.POSITIVE, payload={'action': 'confirm_data', 'answer': True})
    kb.add_button(label='Заполнить заново', color=VkKeyboardColor.NEGATIVE, payload={'action': 'confirm_data', 'answer': False})
    keyboard = kb.get_keyboard()
    send_message(id, 'Спасибо! Проверьте корректность введённых данных\n\n' +
                     '\n'.join(['Имя: ' + user.name, 'Телефон: ' + user.phone, 'Город: ' + user.city, 'Улица: ' + user.street,
                                'Дом: ' + user.building, 'Квартира: ' + user.apartment, 'Этаж: ' + user.floor,
                                'Лифт: ' + ('есть' if user.isElevator else 'отсутствует')]), keyboard=keyboard)


def confirm_data(id, data, option):
    user = RequestUser.get(RequestUser.vk_id == id)
    if option:
        user.isInfo = True
        user.save()
        send_message(id, 'Отлично! Теперь Вы можете оформить заявку на волонтёрскую помощь')
    else:
        get_info(id, data)


def make_request(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.state = 'input_order'
    user.save()
    kb = VkKeyboard(one_time=True)
    kb.add_button(label='Показать популярные', color=VkKeyboardColor.DEFAULT, payload={'action': 'show_popular'})
    keyboard = kb.get_keyboard()
    send_message(id, 'Введите Ваш заказ', keyboard=keyboard)


def show_popular(id, data):
    kb = VkKeyboard(one_time=True)
    kb.add_button(label='Гречка, 1кг', color=VkKeyboardColor.DEFAULT, payload={'action': 'show_popular'})
    kb.add_button(label='Белый хлеб, 1 батон', color=VkKeyboardColor.DEFAULT, payload={'action': 'show_popular'})
    kb.add_line()
    kb.add_button(label='Манка, 500г', color=VkKeyboardColor.DEFAULT, payload={'action': 'show_popular'})
    kb.add_button(label='Яйца, 10 штук', color=VkKeyboardColor.DEFAULT, payload={'action': 'show_popular'})
    kb.add_line()
    kb.add_button(label='Завершить оформление заказа', color=VkKeyboardColor.PRIMARY, payload={'action': 'save_order'})
    keyboard = kb.get_keyboard()
    send_message(id, 'Выберите товар или завершите оформление', keyboard=keyboard)


def input_order(id, data):
    kb = VkKeyboard(one_time=True)
    kb.add_button(label='Продолжить оформление', color=VkKeyboardColor.PRIMARY, payload={'action': 'show_popular'})
    kb.add_button(label='Завершить оформление', color=VkKeyboardColor.DEFAULT, payload={'action': 'save_order'})
    keyboard = kb.get_keyboard()
    send_message(id, 'Выберите дальнейшее действие', keyboard=keyboard)


def save_order(id, data):
    user = RequestUser.get(RequestUser.vk_id == id)
    user.state = 'default'
    user.save()
    send_message(id, 'Ваш заказ №' + str(random.randint(1, 100)) + ' успешно создан ✅\nМы будем информировать Вас о статусе его выполнения!')
