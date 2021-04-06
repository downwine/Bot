from filling_docs import create_dictionary, fill_transfer_document, fill_absence_document, fill_guest_document, \
    fill_relocation_document, send_msg_without_keyboard, vk_session, session_api, send_msg_with_keyboard
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class VkBot:
    """Сам бот, содержащий весь функционал"""

    user_id = None
    USERNAME = None
    COMMANDS = ["ПРИВЕТ", "НАЧАТЬ", "START", "ПОКА", "УСТАЛ", "ОТПРАВИТЬ ЗАЯВЛЕНИЕ", "ОТПРАВИТЬ ЧЕК",
                "НА ВНОС", "НА ОТЪЕЗД", "НА ГОСТЯ", "НА ПЕРЕСЕЛЕНИЕ",
                "СПИСОК КОМАНД", "КОГДА Я ДЕЖУРЮ", "ДОБАВИТЬ", "УДАЛИТЬ"]
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
    def create_docs_keyboard():
        """Создание клавиатуры с выбором документов"""
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('На внос', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('На отъезд', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('На гостя', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('На переселение', color=VkKeyboardColor.PRIMARY)

        return keyboard.get_keyboard()

    @staticmethod
    def send_types_of_docs(self, user_id):
        """Сообщение с клавиатурой документов"""
        vk_session.method('messages.send', {'user_id': user_id,
                                            'message': "Выберите тип заявления:",
                                            'keyboard': self.create_docs_keyboard(),
                                            'random_id': 0})

    @staticmethod
    def get_user_name_from_vk_id(user_id):
        """Получение имени пользователя с помощью идентификатора"""
        return session_api.users.get(user_id=user_id)[0]['first_name']

    @staticmethod
    def get_user_city(user_id):
        """ Получаем город пользователя"""
        return session_api.users.get(user_id=user_id, fields="city")[0]['city']['title']

    def new_message(self, message, user_id):
        """
        Генерация нового сообщения для отправки
        :param user_id: Идентификатор пользователя
        :param message: Входящее сообщение пользователя
        :return: Сообщение от бота
        """

        # Привет или Начать или Start
        if message.upper() in self.COMMANDS[0] or message.upper() == self.COMMANDS[1] \
                or message.upper() == self.COMMANDS[2]:
            send_msg_with_keyboard(user_id,
                                   f"Привет-привет, {self.USERNAME} из города{self.city}!"
                                   f" Если я не отвечаю тебе сразу, то не расстраивайся и повтори своё сообщение "
                                   f"через пару минут")

        # Пока
        elif message.upper() == self.COMMANDS[3]:
            send_msg_without_keyboard(user_id, f"Пока-пока, {self.USERNAME}!")

        # Устал
        elif message.upper() == self.COMMANDS[4]:
            vk_session.method('messages.send', {'user_id': user_id,
                                                'attachment': "https://sun9-63.userapi.com/impf/4qBJys6hFxf01_"
                                                              "fbcYhaRifkynsOK7J81Y4e3Q/A70V_KPPhEA.jpg?size=1920x1274&"
                                                              "quality=96&sign=f493a2a44d93bd9f274f53d110422e10&type=album",
                                                'random_id': 0})

        # Отправить заявление
        elif message.upper() == self.COMMANDS[5]:
            self.send_types_of_docs(self, user_id)

        # Отправить чек
        elif message.upper() == self.COMMANDS[6]:
            print()

        # Заявление на внос
        elif message.upper() == self.COMMANDS[7]:
            d = fill_transfer_document(self, create_dictionary(self))
            print(d)
            if d is not None:
                if len(d) > 3:
                    send_msg_with_keyboard(self.user_id, "Спасибо за заполнение заявления!")

        # Заявление на отъезд
        elif message.upper() == self.COMMANDS[8]:
            d = fill_absence_document(self, create_dictionary(self))
            print(d)
            if d is not None:
                if len(d) > 3:
                    send_msg_with_keyboard(self.user_id, "Спасибо за заполнение заявления!")

        # Заявление на гостя
        elif message.upper() == self.COMMANDS[9]:
            d = fill_guest_document(self, create_dictionary(self))
            print(d)
            if d is not None:
                if len(d) > 3:
                    send_msg_with_keyboard(self.user_id, "Спасибо за заполнение заявления!")

        # Заявление на переселение
        elif message.upper() == self.COMMANDS[10]:
            d = fill_relocation_document(self, create_dictionary(self))
            print(d)
            if d is not None:
                if len(d) > 3:
                    send_msg_with_keyboard(self.user_id, "Спасибо за заполнение заявления!")

        # Список команд
        elif message.upper() == self.COMMANDS[11]:
            send_msg_without_keyboard(user_id, "Список возможных команд: \n"
                                               "Отправить заявление\n"
                                               "Отправить чек\n"
                                               "Когда я дежурю")

        # Когда я дежурю
        elif message.upper() == self.COMMANDS[12]:
            print()

        # Добавить человека в таблицу
        elif message.upper() == self.COMMANDS[13]:
            if self.user_id == 157833436:
                print()

        # Удалить человека из таблицы
        elif message.upper() == self.COMMANDS[14]:
            if self.user_id == 157833436:
                print()

        else:
            send_msg_without_keyboard(user_id, "Не понимаю, о чем вы...")
