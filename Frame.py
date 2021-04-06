from vk_api.longpoll import VkEventType
from vk_bot import VkBot
from filling_docs import longpoll, send_msg_without_keyboard
from Duty_Hours import duty_hours_today, search_id

# Основной цикл
print("Server started")
# Слушаем сервер
flags = [False, False, False, False, False, False, False]
duty_hours_today(flags)
flag = False

for event in longpoll.listen():
    duty_hours_today(flags)
    if event.type == VkEventType.MESSAGE_NEW:  # Если новое сообщение
        if search_id(event.user_id) is not None:
            if event.to_me:  # Для бота
                print('New message:')
                print(f'For me by: {event.user_id}', end='\n')
                bot = VkBot(event.user_id)  # Создаём объект бота
                bot.new_message(event.text, event.user_id)  # Отправляем сообщение
                print('Text: ', event.text)
        else:
            bot = VkBot(event.user_id)
            if not flag:
                send_msg_without_keyboard(event.user_id, "Ты кто такой?")
                flag = True
