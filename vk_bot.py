import requests
from bs4 import BeautifulSoup


def clean_all_tag_from_name(string_line):
    """
    Функция для очистки от тэгов и их содержимых
    :param string_line: строка с именем пользователя
    :return: строка без лишних тэгов, только имя
    """
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result


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

    def __init__(self, user_id):
        """Конструктор"""
        self.USER_ID = user_id
        self.USERNAME = self.get_user_name_from_vk_id(user_id)
        self.COMMANDS = ["ПРИВЕТ", "ДАТА", "ВРЕМЯ", "ПОКА", "НАЧАТЬ", "START"]
        self.url = set_url("https://my-calend.ru/date-and-time-today")

    @staticmethod
    def get_user_name_from_vk_id(user_id):
        """Получение имени пользователя с помощью идентификатора"""
        soup = set_url("https://vk.com/id" + str(user_id))
        user_name = clean_all_tag_from_name(soup.findAll("title")[0])
        return user_name.split()[0]

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
            return f"Привет-привет, {self.USERNAME}!"

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
