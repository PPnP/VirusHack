import csv
import random
import string
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from bots.volunteer import vk
from app.api.models.user import VolunteerUser
from app.api.models.order import Order
from config import fm


def get_default_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Принять заказ', color=VkKeyboardColor.PRIMARY, payload={'action': 'take_order'})
    keyboard.add_button(label='История заказов', color=VkKeyboardColor.DEFAULT, payload={'action': 'orders_history'})
    default_keyboard = keyboard.get_keyboard()
    return default_keyboard


def send_message(id, message, attachment='', keyboard=get_default_keyboard()):
    random_id = int(''.join(random.choice(string.digits) for _ in range(10)))
    vk.messages.send(user_id=id, random_id=random_id, message=message, attachment=attachment, keyboard=keyboard)


def get_info(id, data):
    user = VolunteerUser.get(VolunteerUser.vk_id == id)
    user.state = 'save_location'
    user.save()
    send_message(id, 'Отправьте нам Вашу геолокацию')


def save_location(id, data):
    user = VolunteerUser.get(VolunteerUser.vk_id == id)
    user.state = 'save_distance'
    user.save()
    send_message(id, 'Сколько километров Вы готовы пройти?')


def save_distance(id, data):
    user = VolunteerUser.get(VolunteerUser.vk_id == id)
    user.state = 'save_weights'
    user.save()
    send_message(id, 'Какой вес в килограммах Вы готовы нести?')


def save_weights(id, data):
    data = list()
    with open('alg/experiments/data.txt', 'r') as datafile:
        reader = csv.reader(datafile, delimiter=';')
        for line in reader:
            data.append((line[0], (float(line[1]), float(line[2]))))

    for shop in data:
        fm.add_shop(shop)

    fm.add_w('Гречка 1 кг', 1.05)
    fm.add_c('Гречка 1 кг', 65)
    fm.add_w('Хлеб белый нарезной', 0.250)
    fm.add_c('Хлеб белый нарезной', 36)
    fm.add_w('Манка 500 гр', 0.250)
    fm.add_c('Манка 500 гр', 47)
    fm.add_w('Вода 5 л', 5.1)
    fm.add_c('Вода 5 л', 90)
    fm.add_w('Хлеб черный нарезной', 0.25)
    fm.add_c('Хлеб черный нарезной', 40)
    fm.add_w('Печенье', .2)
    fm.add_c('Печенье', 25)
    fm.add_task('Алиса Антоновна', 'Ленина д 5, кв 92', (54.190455, 37.618487), 4, False, '+79851234567',
                [('Хлеб белый нарезной', 2), ('Гречка 1 кг', 1)])
    fm.add_task('Боб Борисович', 'ул. Ильича, д. 1, кв 6341', (54.191337, 37.617067), 12, True, '+79167654321',
                [('Хлеб белый нарезной', 1), ('Манка 500 гр', 1), ('Печенье', 4)])
    fm.add_task('Валерий Виссарионович', 'ул. Ильича, д. 13, кв 5', (54.192874, 37.620233), 1, False, '+791699999999',
                [('Хлеб белый нарезной', 2), ('Хлеб черный нарезной', 1)])
    fm.add_task('Глеб Григорьевич', 'проспект Жукова д 24, кв 32', (54.190386, 37.621767), 3, True, '+79168888888',
                [('Вода 5 л', 2)])

    txt, ids = fm.volunteer_to_path((54.191, 37.619), 4, 1)
    kb = VkKeyboard(one_time=True)
    kb.add_button(label='Да', color=VkKeyboardColor.POSITIVE, payload={'action': 'confirm_order', 'answer': True})
    kb.add_button(label='Нет', color=VkKeyboardColor.NEGATIVE, payload={'action': 'confirm_order', 'answer': False})
    keyboard = kb.get_keyboard()
    send_message(id, txt + '\n\nПодтверждаете заказ?', keyboard=keyboard)
    fm.confirm(ids)


def confirm_order(id, data, answer):
    if answer:
        send_message(id, 'Вам назначен заказ №' + str(random.randint(1, 100)) + ' ✅')
    else:
        send_message(id, 'Выбор заказа отменён')
