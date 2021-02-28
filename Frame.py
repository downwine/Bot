import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import VkBot

# API-ключ
token = "5e57c513cb3a1c9e62eedf59de73e62ec4bc4688d62c1b7508912a146370d929dbef3af9897246fe3c1d3"

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


# Функция отправки сообщений
def send_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


# Основной цикл
print("Server started")
# Слушаем сервер
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW: # Если новое сообщение
        if event.to_me:  # Для бота
            print('New message:')
            print(f'For me by: {event.user_id}', end='\n')
            bot = VkBot(event.user_id)
            send_msg(event.user_id, bot.new_message(event.text))
            print('Text: ', event.text)
