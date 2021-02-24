import requests
import bs4


class VkBot:

    @staticmethod
    def set_http(http: str):
        request = requests.get(http)
        bs = bs4.BeautifulSoup(request.text, "html.parser")
        return bs

    # Метод для очистки от ненужных тэгов
    @staticmethod
    def clean_all_tag_from_str(string_line):
        # Очистка строки stringLine от тэгов и их содержимых
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += str(i)
            else:
                if i == ">":
                    not_skip = True
        return result

    def __init__(self, user_id):
        print("Создан объект бота!")
        self._USER_ID = user_id
        self._USERNAME = self.get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"]
        # self.b = self.set_http("https://my-calend.ru/date-and-time-today")
        # self._date = self.clean_all_tag_from_str(self.b.select(".page")[0].findAll("h2")[0]).split(",")
        # self._day_of_week = self._date[1]

    def get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self.clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]
    """
    def get_date(self):
        return self._date[0] + self._date[1]

    def get_day_of_week(self):
        return self._date[1]

    # Получение времени:
    def get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self.clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    # Получение погоды
    @staticmethod
    def get_weather() -> list:

        request = requests.get("https://sinoptik.com.ru/погода-москва")
        b = bs4.BeautifulSoup(request.text, "html.parser")

        p3 = b.select('.temperature .p3')
        weather1 = p3[0].getText()
        p4 = b.select('.temperature .p4')
        weather2 = p4[0].getText()
        p5 = b.select('.temperature .p5')
        weather3 = p5[0].getText()
        p6 = b.select('.temperature .p6')
        weather4 = p6[0].getText()

        result = ''
        result = result + ('Утром :' + weather1 + ' ' + weather2) + '\n'
        result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
        temp = b.select('.rSide .description')
        weather = temp[0].getText()
        result = result + weather.strip()

        return result
    """
    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Погода
        elif message.upper() == self._COMMANDS[1]:
            return self.get_weather()

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self.get_time

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        else:
            return "Не понимаю о чем вы..."
