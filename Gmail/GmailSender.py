import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class GmailSender:
    def __init__(self, login='projectbotmailing@gmail.com', password='Y3TbKYpru3i'):
        self.login = login
        self.password = password
        self.DOMAIN = 'smtp.gmail.com'
        self.PORT = 587

    def send_message(self, recipient, message='TestMessage'):
        message = message.encode('utf-8')
        smtpObj = smtplib.SMTP(self.DOMAIN, self.PORT)
        smtpObj.starttls()
        smtpObj.login(self.login, self.password)
        smtpObj.sendmail(self.login, recipient, message)
        smtpObj.quit()

    def send_document(self, recipient, body, file_path, file_name=None):
        # cutting file_path
        if not file_name:
            file_name = file_name = file_path.split('/')[-1].split('\\')[-1]

        message = MIMEMultipart()
        message["From"] = self.login
        message["To"] = recipient
        message["Subject"] = file_name

        message.attach(MIMEText(body, "plain"))

        with open(file_path, "rb") as attachment:
            # Заголовок письма application/octet-stream
            # Почтовый клиент обычно может загрузить это автоматически в виде вложения
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Шифровка файла под ASCII символы для отправки по почте
        # Внесение заголовка в виде пара/ключ к части вложения
        # some_short_path = 'PIS.docx'

        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment', filename=file_name)
        encoders.encode_base64(part)

        print(file_name)

        message.attach(part)
        text = message.as_string()

        self.send_message(recipient, message=text)

    def send_photo(self, recipient, file_path, body='', file_name=None):
        if not file_name:
            file_name = file_name = file_path.split('/')[-1].split('\\')[-1]

        img_data = open(file_path, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Your MoM'
        msg['From'] = 'Your Mom'
        msg['To'] = 'Your Mom'

        text = MIMEText("test")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(file_name))
        msg.attach(image)

        text = msg.as_string()

        self.send_message(recipient, message=text)


#if __name__ == '__main__':
    #gs = GmailSender()
    #gs.send_photo(recipient='down.wine@yandex.ru',
                  #file_path='C:/Users/asus/PycharmProjects/Bot/DocEdit/DocSample/some_cat.jpg')
