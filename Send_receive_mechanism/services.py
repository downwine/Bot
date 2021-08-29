import time
import pathlib
from Send_receive_mechanism.filling_docs import longpoll, send_msg_without_keyboard, send_msg_with_keyboard, vk_session
from vk_api.longpoll import VkEventType

dir_path = pathlib.Path.cwd()


def change_comend_ID(self):
    parsed = False
    j = 0
    delay = 3
    vk_session.method('messages.send', {'user_id': self.user_id,
                                        'message': "Введите ID коменданта (число)",
                                        'random_id': 0})

    for j in range(10):
        for event in longpoll.check():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    if any(map(str.isdigit, event.text)):
                        self.comend_id = event.text
                        lines = []
                        with open("our_token.py", "r") as file:
                            for line in file:
                                if "comend_ID = " in line:
                                    lines.append("comend_ID = " + event.text + "\n")
                                    continue
                                else:
                                    lines.append(line)

                        with open("our_token.py", 'w') as f:
                            for item in lines:
                                f.write("%s" % item)
                        parsed = True
                        break
                    else:
                        send_msg_without_keyboard(self.user_id,
                                                  "ID введён некорректно, повторите ввод")
                        break
        if parsed:
            break
        time.sleep(delay)

    if j == 9:
        send_msg_with_keyboard(self.user_id,
                               "Вы отвечали слишком долго, я не дождался, повторите запрос ещё раз")
        return None

    return True
