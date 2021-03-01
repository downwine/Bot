import requests
from bs4 import BeautifulSoup
import vk_api.vk_api

# API-ключ
token = "5e57c513cb3a1c9e62eedf59de73e62ec4bc4688d62c1b7508912a146370d929dbef3af9897246fe3c1d3"
# Для Long Poll
vk_session = vk_api.VkApi(token=token)
# Для вызова методов vk_api
session_api = vk_session.get_api()


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


def send_msg(user_id, message):
    """Функция для отправки пользователю сообщения"""
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


class VkBot:
    """Сам бот, содержащий весь функционал"""

    user_id = None
    USERNAME = None
    url = None
    COMMANDS = ["ПРИВЕТ", "ДАТА", "ВРЕМЯ", "ПОКА", "НАЧАТЬ", "START"]
    city = None

    def __init__(self, user_id):
        """Конструктор"""
        # Из предыдущего файла импортирую две переменные
        self.user_id = user_id
        self.USERNAME = self.get_user_name_from_vk_id(user_id)
        self.city = self.get_user_city(user_id)

    @staticmethod
    def get_user_name_from_vk_id(user_id):
        """Получение имени пользователя с помощью идентификатора"""
        return session_api.users.get(user_id=user_id)[0]['first_name']

    @staticmethod
    def get_user_city(user_id):
        """ Получаем город пользователя"""
        return session_api.users.get(user_id=user_id, fields="home_town")[0]['home_town']

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

    def new_message(self, message):
        """
        Генерация нового сообщения для отправки
        :param message: Входящее сообщение пользователя
        :return: Сообщение от бота
        """
        # Привет
        if message.upper() in self.COMMANDS[0]:
            return f"Привет-привет, {self.USERNAME} из города {self.city}!"

        # Дата
        elif message.upper() == self.COMMANDS[1]:
            return self.get_date(set_url("https://my-calend.ru/date-and-time-today"))

        # Время
        elif message.upper() == self.COMMANDS[2]:
            return self.get_time(set_url("https://my-calend.ru/date-and-time-today"))

        # Пока
        elif message.upper() == self.COMMANDS[3]:
            return f"Пока-пока, {self.USERNAME}!"

        # Начало
        elif message.upper() == self.COMMANDS[4] or message.upper() == self.COMMANDS[5]:
            return f"Введите ваши реальные имя и фамилию"
            # проверка с базой данных и создание

        else:
            return "Не понимаю о чем вы..."
