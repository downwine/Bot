import requests
from bs4 import BeautifulSoup
import re


def clean_all_tag_from_name(string_line):
    # Очистка строки stringLine от тэгов и их содержимых
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


# Задание вэб-страницы
def set_url(website: str):
    # Посылаем запрос на страницу
    page = requests.get(website)
    # print(page.status_code) 200 - удачное подключение
    # Скармливаем bs4 страницу, в переменной soup весь html-код
    soup = BeautifulSoup(page.text, "html.parser")
    return soup


class VkBot:

    # Конструктор
    def __init__(self, user_id):
        self.USER_ID = user_id
        self.USERNAME = self.get_user_name_from_vk_id(user_id)
        self.COMMANDS = ["ПРИВЕТ", "ДАТА", "ВРЕМЯ", "ПОКА", "НАЧАТЬ", "START"]
        self.url = set_url("https://my-calend.ru/date-and-time-today")

    # Имя пользователя
    @staticmethod
    def get_user_name_from_vk_id(user_id):
        soup = set_url("https://vk.com/id" + str(user_id))
        user_name = clean_all_tag_from_name(soup.findAll("title")[0])
        return user_name.split()[0]

    # Время
    @staticmethod
    def get_time(soup):
        # Записываем в строку тот тэг, который нам нужен
        time = soup.find('h2')
        # result - итог, text - текст тэга
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

    # Дата
    @staticmethod
    def get_date(soup):
        date = soup.find('h2')
        result = ""
        text = date.text
        if "Время" in text:
            j = text.find("Время")
            for i in range(j):
                result += text[i]
        return result

    def new_message(self, message):
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
