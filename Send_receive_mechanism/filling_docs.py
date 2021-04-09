import time
import re
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from DocEdit.regular_expressions import reformat_mobile, full_name_processing
from our_token import token
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Duty.Duty_Hours import search_id

# Для Long Poll
vk_session = vk_api.VkApi(token=token)
# Для вызова методов vk_api
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session, wait=1)


def create_default_keyboard():
    """Создание дефолтной клавиатуры"""
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Отправить заявление', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Отправить чек', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Когда я дежурю?', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Список команд', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def send_msg_with_keyboard(user_id, message):
    """Функция для отправки пользователю сообщения с клавиатурой"""
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'keyboard': create_default_keyboard(),
                                        'random_id': 0})


def send_msg_without_keyboard(user_id, message):
    """Функция для отправки пользователю сообщения без клавиатуры"""
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': 0})


def check_room_number(self, text):
    """
    Функция для проверки корректности введения номера комнаты
    :param text: то, что надо проверить
    :return: True, если всё правильно
    """
    if not text.isdigit() or 201 > int(text) or int(text) > 918:
        send_msg_without_keyboard(self.user_id,
                                  "Номер комнаты введён некорректно, повторите ввод")
        return False

    return True


def check_date(self, text):
    """
    Функция для проверки корректности введения даты
    :param text: то, что надо проверить
    :return: True, если всё правильно
    """
    if (re.search(pattern=r'[^0-9\.]', string=text) is not None) or len(text) != 8:
        send_msg_without_keyboard(self.user_id,
                                  "Дата введена некорректно, повторите ввод")
        return False

    return True


def create_dictionary(self):
    """
    Функция для получения первых общих ответов от пользователя
    :param self: объект бота
    :return: словарь с двумя ответами
    """
    send_msg_without_keyboard(self.user_id,
                              "Перед заполнением Вы можете ознакомиться с шаблонами по ссылке "
                              "https://vk.com/album-202823499_277877657")
    answers = []
    mess = ["Введите номер комнаты, в которой проживаете",
            "Введите контактный телефон"]
    user_fio = search_id(self.user_id)
    answers.append(user_fio)

    for i in range(2):
        send_msg_without_keyboard(self.user_id, mess[i])
        parsed = False
        j = 0
        delay = 3
        for j in range(10):
            for event in longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        temp = event.text
                        if i == 0:
                            if not check_room_number(self, event.text):
                                break
                        if i == 1:
                            temp = reformat_mobile(event.text)
                            if temp is None:
                                send_msg_without_keyboard(self.user_id,
                                                          "Номер телефона введён некорректно, повторите ввод")
                                break

                        answers.append(temp)
                        parsed = True

            time.sleep(delay)
            if parsed:
                break

        if j == 9:
            send_msg_with_keyboard(self.user_id,
                                   "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
            return None

    return answers


def fill_current_date(self, dict_keys, answers):
    """
    Функция для довавления даты заполнения заявления и завершения формирования словаря
    :param dict_keys: промежуточные ключи
    :param answers: промежуточные ответы
    :return: готовый заполненный словарь
    """
    send_msg_without_keyboard(self.user_id, "Введите дату заполнения в формате дд.мм.гг")
    parsed = False
    j = 0
    delay = 3
    for j in range(10):
        for event in longpoll.check():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if not check_date(self, event.text):
                        break
                    dict_keys.append("current_date")
                    answers.append(event.text)
                    parsed = True
                    break

        time.sleep(delay)
        if parsed:
            break

    if j == 9:
        send_msg_with_keyboard(self.user_id,
                               "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
        return None

    dict_of_answers = dict(zip(dict_keys, answers))

    return dict_of_answers


def fill_transfer_document(self, answers):
    """
    Функция для заполнения заявления на внос
    :param answers: первоначальный словарь ответов
    :return: готовый словарь ответов
    """
    if answers is None:
        return None

    fields = ["Введите дату, когда хотите внести/вынести вещи, в формате дд.мм.гг",
              "Вы желаете осуществить внос или вынос?",
              "Перечислите через запятую вещи, которые хотите внести/вынести",
              "Введите через запятую соседей, с которыми согласован внос/вынос"]
    dict_keys = ["full_name", "room_number", "phone_number", "date_of_moving", "in_or_out",
                 "list_of_items", "neighbors"]

    for i in range(len(fields)):
        send_msg_without_keyboard(self.user_id, fields[i])
        parsed = False
        j = 0
        delay = 3
        for j in range(10):
            for event in longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if i == 0:
                            if not check_date(self, event.text):
                                break
                        if i == 1:
                            if event.text.upper() != "ВНОС" and event.text.upper() != "ВЫНОС":
                                send_msg_without_keyboard(self.user_id,
                                                          "Ввод некорректен, повторите ввод")
                                break

                        answers.append(event.text)
                        parsed = True
                        break
            if parsed:
                break
            time.sleep(delay)

        if j == 9:
            send_msg_with_keyboard(self.user_id,
                                   "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
            return None

    return fill_current_date(self, dict_keys, answers)


def fill_absence_document(self, answers):
    """
    Функция для заполнения заявления на отсутствие
    :param answers: первоначальный словарь ответов
    :return: готовый словарь ответов
    """
    if answers is None:
        return None

    fields = ["Введите период, начиная с которого Вы будете отсутствовать, в формате дд.мм.гг",
              "Введите период, по который вы будете отсутствовать, в формате дд.мм.гг",
              "Введите причину отсутствия"]
    dict_keys = ["full_name", "room_number", "phone_number", "period_from", "period_to",
                 "reason"]

    for i in range(len(fields)):
        send_msg_without_keyboard(self.user_id, fields[i])
        parsed = False
        j = 0
        delay = 3
        for j in range(10):
            for event in longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if i == 0 or i == 1:
                            if not check_date(self, event.text):
                                break

                        answers.append(event.text)
                        parsed = True
                        break
            if parsed:
                break
            time.sleep(delay)

        if j == 9:
            send_msg_with_keyboard(self.user_id,
                                   "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
            return None

    return fill_current_date(self, dict_keys, answers)


def fill_guest_document(self, answers):
    """
    Функция для заполнения заявления на гостя
    :param answers: первоначальный словарь ответов
    :return: готовый словарь ответов
    """
    if answers is None:
        return None

    fields = ["Введите ФИО гостя, которого приглашаете",
              "Введите номер комнаты, в которую приглашаете",
              "Введите дату, в которую хотите пригласить гостя, в формате дд.мм.гг",
              "Введите время, начиная с которого гость будет присутствовать",
              "Введите время, по которое гость будет присутствовать",
              "Введите через запятую ФИО соседей, с которыми согласован проход гостя"]
    dict_keys = ["full_name", "room_number", "phone_number", "guest_name", "invitation_room",
                 "day_of_visit", "time_from", "time_to", "neighbors"]

    for i in range(len(fields)):
        send_msg_without_keyboard(self.user_id, fields[i])
        parsed = False
        j = 0
        delay = 3
        for j in range(10):
            for event in longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        temp = event.text
                        if i == 0:
                            temp = full_name_processing(event.text)
                            if temp is None:
                                send_msg_without_keyboard(self.user_id, "ФИО введены некорректно, повторите ввод")
                                break
                        if i == 1:
                            if not check_room_number(self, event.text):
                                break
                        if i == 2:
                            if not check_date(self, event.text):
                                break
                        if i == 3 or i == 4:
                            if len(event.text) != 5:
                                send_msg_without_keyboard(self.user_id,
                                                          "Время введено некорректно, повторите ввод")
                                break

                        answers.append(temp)
                        parsed = True
                        break
            if parsed:
                break
            time.sleep(delay)

        if j == 9:
            send_msg_with_keyboard(self.user_id,
                                   "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
            return None

    return fill_current_date(self, dict_keys, answers)


def fill_relocation_document(self, answers):
    """
    Функция для заполнения заявления на переселение
    :param answers: первоначальный словарь ответов
    :return: готовый словарь ответов
    """
    if answers is None:
        return None

    fields = ["Введите комнату, в которую хотите переселиться",
              "Введите комнату, из которой хотите переселиться",
              "Введите причину",
              "Есть ли у вас академическая задолженность? Да / Нет",
              "Имеете ли вы дисциплинарные высказывания? Да / Нет",
              "Введите через запятую ФИО соседей, с которыми было согласовано посещение"]
    dict_keys = ["full_name", "room_number", "phone_number", "room_to", "room_from",
                 "reason", "academ_debt", "reprimands", "neighbors"]

    for i in range(len(fields)):
        send_msg_without_keyboard(self.user_id, fields[i])
        parsed = False
        j = 0
        delay = 3
        for j in range(10):
            for event in longpoll.check():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if i == 0 or i == 1:
                            if not check_room_number(self, event.text):
                                break

                        if i == 3 or i == 4:
                            if (event.text.upper() != "ДА") and (event.text.upper() != "НЕТ"):

                                send_msg_without_keyboard(self.user_id,
                                                          "Ввод некорректен, повторите ввод")
                                break

                        answers.append(event.text)
                        parsed = True
                        break
            if parsed:
                break
            time.sleep(delay)

        if j == 9:
            send_msg_with_keyboard(self.user_id,
                                   "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
            return None

    return fill_current_date(self, dict_keys, answers)


def taking_str(self):
    """
    Функция для получения строки от пользователя
    :param self: объект бота
    :return: полученный текст
    """
    text = None
    parsed = False
    j = 0
    delay = 3
    for j in range(10):
        for event in longpoll.check():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    text = event.text
                    parsed = True
        time.sleep(delay)
        if parsed:
            break
    if j == 9:
        send_msg_with_keyboard(self.user_id,
                               "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
        return None
    return text
