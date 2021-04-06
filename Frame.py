from vk_api.longpoll import VkEventType
from vk_bot import VkBot
from filling_docs import longpoll

# Основной цикл
print("Server started")
# Слушаем сервер

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:  # Если новое сообщение
        if event.to_me:  # Для бота
            print('New message:')
            print(f'For me by: {event.user_id}', end='\n')
            bot = VkBot(event.user_id)  # Создаём объект бота
            bot.new_message(event.text, event.user_id)  # Отправляем сообщение
            print('Text: ', event.text)
