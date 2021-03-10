import requests
from bs4 import BeautifulSoup
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import re

# API-ключ
token = "5e57c513cb3a1c9e62eedf59de73e62ec4bc4688d62c1b7508912a146370d929dbef3af9897246fe3c1d3"
# Для Long Poll
vk_session = vk_api.VkApi(token=token)
# Для вызова методов vk_api
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def mobile_valid_check(phone_number):
    """
    valid phone check
    :param: phone_number: phone_number
    :return: bool: is number valid
    """

    pattern = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
    letters = re.compile(r'[^0-9-+() ]')

    if letters.search(phone_number):
        return False

    phone_number = phone_number.replace(' ', '')
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(')', '')
    phone_number = phone_number.replace('(', '')

    return True if pattern.search(phone_number) else False


def set_url(website: str):
    """
    Задание вэб-страницы для объекта бота
    :param website: url сайта в интернете
    :return: html код сайта
    """
    # Посылаем запрос на страницу
    page = requests.get(website)
    # print(page.status_code) 200 - удачное подключение
    # Скармливаем bs4 страницу, в переменной soup весь html-код
    soup = BeautifulSoup(page.text, "html.parser")

    return soup


class VkBot:
    """Сам бот, содержащий весь функционал"""

    user_id = None
    USERNAME = None
    url = None
    COMMANDS = ["ПРИВЕТ", "ДАТА", "ВРЕМЯ", "ПОКА", "НАЧАТЬ", "START", "УСТАЛ", "ОТПРАВИТЬ ЗАЯВЛЕНИЕ", "ОТПРАВИТЬ ЧЕК",
                "ЗАЯВЛЕНИЕ НА ВНОС", "ЗАЯВЛЕНИЕ НА ОТЪЕЗД", "ЗАЯВЛЕНИЕ НА ГОСТЯ", "ЗАЯВЛЕНИЕ НА ПЕРЕСЕЛЕНИЕ"]
    city = None

    def __init__(self, user_id):
        """Конструктор"""
        # Из предыдущего файла импортирую две переменные
        self.user_id = user_id
        self.USERNAME = self.get_user_name_from_vk_id(user_id)
        try:
            self.city = " " + self.get_user_city(user_id)
        except KeyError:
            self.city = ", который не указан"

    @staticmethod
    def create_default_keyboard():
        """Создание дефолтной клавиатуры"""
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button('Отправить заявление', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Отправить чек', color=VkKeyboardColor.PRIMARY)

        return keyboard.get_keyboard()

    @staticmethod
    def create_docs_keyboard():
        """Создание клавиатуры с выбором документов"""
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Заявление на внос', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Заявление на отъезд', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Заявление на гостя', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Заявление на переселение', color=VkKeyboardColor.PRIMARY)

        return keyboard.get_keyboard()

    @staticmethod
    def send_msg_with_keyboard(self, user_id, message):
        """Функция для отправки пользователю сообщения с клавиатурой"""
        vk_session.method('messages.send', {'user_id': user_id,
                                            'message': message,
                                            'keyboard': self.create_default_keyboard(),
                                            'random_id': 0})

    @staticmethod
    def send_types_of_docs(self, user_id):
        """Сообщение с клавиатурой документов"""
        vk_session.method('messages.send', {'user_id': user_id,
                                            'message': "Выберите тип заявления:",
                                            'keyboard': self.create_docs_keyboard(),
                                            'random_id': 0})

    @staticmethod
    def get_current_date(self, mess, dict_keys, answers):
        send_msg_without_keyboard(self.user_id, mess[3])
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.user_id == self.user_id:
                if event.to_me:
                    if len(event.text) != 8:
                        send_msg_without_keyboard(self.user_id,
                                                  "Дата введена некорректно, повторите ввод")
                        continue
                    dict_keys.append("current_date")
                    answers.append(event.text)
                    break
        dict_of_answers = dict(zip(dict_keys, answers))

        return dict_of_answers

    @staticmethod
    def create_dictionary(self, doc_id):
        send_msg_without_keyboard(self.user_id,
                                  "Перед заполнением Вы можете ознакомиться с шаблонами по ссылке "
                                  "https://vk.com/album-202823499_277877657")
        answers = []
        mess = ["Введите свои имя, фамилию и отчество в родительном падеже",
                "Введите номер комнаты, в которой проживаете",
                "Введите контактный телефон",
                "Введите дату заполнения в формате дд.мм.гг"]

        for i in range(3):
            send_msg_without_keyboard(self.user_id, mess[i])
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        if i == 0:
                            if len(event.text.split(" ")) < 2:
                                send_msg_without_keyboard(self.user_id, "ФИО введены некорректно, повторите ввод")
                                continue
                        if i == 1:
                            if 201 > int(event.text) or int(event.text) > 918:
                                send_msg_without_keyboard(self.user_id,
                                                          "Номер комнаты введён некорректно, повторите ввод")
                                continue
                        if i == 2:
                            if not mobile_valid_check(event.text):
                                send_msg_without_keyboard(self.user_id,
                                                          "Номер телефона введён некорректно, повторите ввод")
                                continue

                        answers.append(event.text)
                        break

        if doc_id == 0:
            fields = ["Введите дату, когда хотите внести/вынести вещи, в формате дд.мм.гг",
                      "Заявление на внос или на вынос?",
                      "Перечислите через запятую вещи, которые хотите внести/вынести",
                      "Введите через запятую соседей, с которыми согласован внос/вынос"]
            dict_keys = ["full_name", "room_number", "phone_number", "date_of_moving", "in_or_out",
                         "list_of_items", "neighbors"]

            for i in range(len(fields)):
                send_msg_without_keyboard(self.user_id, fields[i])
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.user_id == self.user_id:
                        if event.to_me:
                            if i == 0:
                                if len(event.text) != 8:
                                    send_msg_without_keyboard(self.user_id,
                                                              "Дата введена некорректно, повторите ввод")
                                    continue
                            if i == 1:
                                if event.text.upper() != "ВНОС" or event.text.upper() != "ВЫНОС":
                                    send_msg_without_keyboard(self.user_id,
                                                              "Ввод некорректен, повторите ввод")
                                    continue
                            if i == 3 or i == 2:
                                string = event.text.split(", ")
                                answers.append(string)
                            else:
                                answers.append(event.text)
                            break

            return self.get_current_date(self, mess, dict_keys, answers)

        elif doc_id == 1:
            fields = ["Введите период, начиная с которого Вы будете отсутствовать, в формате дд.мм.гг",
                      "Введите период, по который вы будете отсутствовать, в формате дд.мм.гг",
                      "Введите причину отсутствия"]
            dict_keys = ["full_name", "room_number", "phone_number", "period_from", "period_to",
                         "reason"]

            for i in range(len(fields)):
                send_msg_without_keyboard(self.user_id, fields[i])
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.user_id == self.user_id:
                        if event.to_me:
                            if i == 0 or i == 1:
                                if len(event.text) != 8:
                                    send_msg_without_keyboard(self.user_id,
                                                              "Дата введена некорректно, повторите ввод")
                                    continue
                            answers.append(event.text)
                            break

            return self.get_current_date(self, mess, dict_keys, answers)

        elif doc_id == 2:
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
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.user_id == self.user_id:
                        if event.to_me:
                            if i == 0:
                                if len(event.text.split(" ")) < 2:
                                    send_msg_without_keyboard(self.user_id,
                                                              "ФИО введены некорректно, повторите ввод")
                                    continue
                            if i == 1:
                                if 201 > int(event.text) or int(event.text) > 918:
                                    send_msg_without_keyboard(self.user_id,
                                                              "Номер комнаты введён некорректно, повторите ввод")
                                    continue
                            if i == 2:
                                if len(event.text) != 8:
                                    send_msg_without_keyboard(self.user_id,
                                                              "Дата введена некорректно, повторите ввод")
                                    continue
                            if i == 3 or i == 4:
                                if not event.text.isdigit():
                                    send_msg_without_keyboard(self.user_id,
                                                              "Время введено некорректно, повторите ввод")
                                    continue
                            if i == 5:
                                string = event.text.split(", ")
                                answers.append(string)
                            else:
                                answers.append(event.text)
                            break

            return self.get_current_date(self, mess, dict_keys, answers)

        elif doc_id == 3:
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
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.user_id == self.user_id:
                        if event.to_me:
                            if i == 0 or i == 1:
                                if 201 > int(event.text) or int(event.text) > 1000:
                                    send_msg_without_keyboard(self.user_id,
                                                              "Номер комнаты введён некорректно, повторите ввод")
                                    continue
                            if i == 3 or i == 4:
                                if event.text.upper() == "ДА":
                                    answers.append(True)
                                elif event.text.upper() == "НЕТ":
                                    answers.append(False)
                                else:
                                    send_msg_without_keyboard(self.user_id,
                                                              "Ввод некорректен, повторите ввод")
                                    continue
                            if i == 5:
                                string = event.text.split(", ")
                                answers.append(string)
                            else:
                                answers.append(event.text)
                            break

            return self.get_current_date(self, mess, dict_keys, answers)

    @staticmethod
    def get_user_name_from_vk_id(user_id):
        """Получение имени пользователя с помощью идентификатора"""
        return session_api.users.get(user_id=user_id)[0]['first_name']

    @staticmethod
    def get_user_city(user_id):
        """ Получаем город пользователя"""
        return session_api.users.get(user_id=user_id, fields="city")[0]['city']['title']

    @staticmethod
    def get_time(soup):
        """
        Получение текущего времени
        :param soup: html код страницы
        :return: текущее время, строка
        """
        # Записываем в строку тот тэг, который нам нужен
        time = soup.find('h2')
        # text - текст тэга
        result = ""
        text = time.text
        # Отделяем время от даты
        if "Время" in text:
            j = text.find("Время")
            for i in range(len(text)):
                if i == j:
                    result += text[j]
                    j += 1

        return result

    @staticmethod
    def get_date(soup):
        """
        Получение текущей даты
        :param soup: html код страницы
        :return: текущая дата, строка
        """
        date = soup.find('h2')
        result = ""
        text = date.text
        if "Время" in text:
            j = text.find("Время")
            for i in range(j):
                result += text[i]
        return result

    def new_message(self, message, user_id):
        """
        Генерация нового сообщения для отправки
        :param user_id: Идентификатор пользователя
        :param message: Входящее сообщение пользователя
        :return: Сообщение от бота
        """
        # Привет
        if message.upper() in self.COMMANDS[0]:
            self.send_msg_with_keyboard(self, user_id,
                                        f"Привет-привет, {self.USERNAME} из города{self.city}!"
                                        f" Если я не отвечаю тебе сразу, то не расстраивайся и повтори своё сообщение "
                                        f"через пару минут")

        # Дата
        elif message.upper() == self.COMMANDS[1]:
            self.send_msg_with_keyboard(self, user_id,
                                        self.get_date(set_url("https://my-calend.ru/date-and-time-today")))

        # Время
        elif message.upper() == self.COMMANDS[2]:
            self.send_msg_with_keyboard(self, user_id,
                                        self.get_time(set_url("https://my-calend.ru/date-and-time-today")))

        # Пока
        elif message.upper() == self.COMMANDS[3]:
            send_msg_without_keyboard(user_id, f"Пока-пока, {self.USERNAME}!")

        # Начало
        elif message.upper() == self.COMMANDS[4] or message.upper() == self.COMMANDS[5]:
            send_msg_without_keyboard(user_id, "Введите ваши реальные имя и фамилию")
            # проверка с базой данных и регистрация

        # Устал
        elif message.upper() == self.COMMANDS[6]:
            vk_session.method('messages.send', {'user_id': user_id,
                                                'attachment': "https://sun9-63.userapi.com/impf/4qBJys6hFxf01_"
                                                              "fbcYhaRifkynsOK7J81Y4e3Q/A70V_KPPhEA.jpg?size=1920x1274&"
                                                              "quality=96&sign=f493a2a44d93bd9f274f53d110422e10&type=album",
                                                'random_id': 0})

        # Отправить заявление
        elif message.upper() == self.COMMANDS[7]:
            self.send_types_of_docs(self, user_id)

        # Отправить чек
        elif message.upper() == self.COMMANDS[8]:
            print()

        # Заявление на внос
        elif message.upper() == self.COMMANDS[9]:
            a = self.create_dictionary(self, 0)
            print(a)

        # Заявление на отъезд
        elif message.upper() == self.COMMANDS[10]:
            a = self.create_dictionary(self, 1)
            print(a)

        # Заявление на гостя
        elif message.upper() == self.COMMANDS[11]:
            a = self.create_dictionary(self, 2)
            print(a)

        # Заявление на переселение
        elif message.upper() == self.COMMANDS[12]:
            a = self.create_dictionary(self, 3)
            print(a)

        else:
            send_msg_without_keyboard(user_id, "Не понимаю о чем вы...")


def send_msg_without_keyboard(user_id, message):
    """Функция для отправки пользователю сообщения без клавиатуры"""
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': 0})
