import smtplib
from email import encoders
from email.mime.base import MIMEBase
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

    def send_gmail(self, recipient, body, file_path, file_name=None):
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
