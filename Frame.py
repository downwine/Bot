from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import VkBot, token, vk_session, longpoll, send_msg_without_keyboard
import time

# Основной цикл
print("Server started")
# Слушаем сервер
"""
start_time = time.time()
end_time = time.time()
        if end_time - start_time > 5.0:
            send_msg_without_keyboard(event.id, "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
            break
"""

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:  # Если новое сообщение
        if event.to_me:  # Для бота
            print('New message:')
            print(f'For me by: {event.user_id}', end='\n')
            bot = VkBot(event.user_id)  # Создаём объект бота
            bot.new_message(event.text, event.user_id)  # Отправляем сообщение
            print('Text: ', event.text)
