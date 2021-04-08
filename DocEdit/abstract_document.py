from docxtpl import DocxTemplate
from docxtpl import RichText
import datetime
import os

from Gmail.GmailSender import GmailSender


class AbstractDocument:
    def __init__(self, path_to_sample, path_to_save):
        # print(os.getcwd())
        if __name__ == '__main__':
            print(__name__)

        self.path_to_sample = path_to_sample
        self.path_to_save = path_to_save
        self.last_file_path = None
        self.document = DocxTemplate(self.path_to_sample)  # reading document with __init__ path param

        if self.__docname__ is None:
            self.__docname__ = 'Abstract'

    def __name__(self):
        return self.__docname__

    def write_usual(self, document_context_kwargs):
        """
            Multiple render and file saver
            :param document_context_kwargs - dict of {{ vars }} and their values
            :return: self.last_file_path - storing path ro the last file
        """
        # checking validity
        self.check(document_context_kwargs)

        # saving full_name and date for file saving
        full_name = document_context_kwargs['full_name']
        date = document_context_kwargs['current_date']

        self.preprocess_dict(document_context_kwargs)

        # rendering document
        self.document.render(document_context_kwargs)

        # storing last_file_path
        self.last_file_path = self.preprocess_path_to_save(full_name)
        # saves file to the last_path
        self.save()

        return self.last_file_path

    def preprocess_dict(self, document_context_kwargs):
        """
        preprocessing of some dict values
        :param document_context_kwargs:
        :return: None
        """
        # preprocessing values
        # document_context_kwargs['current_date'] = self.preprocess_date(document_context_kwargs['current_date'])
        document_context_kwargs['initials'] = self.preprocess_full_name(document_context_kwargs['full_name'])

    def write_rich(self, text_variable, text_content, render_italic=False,
                   render_underlined=False, render_bold=False, render_color='#000000',
                   render_size=24, render_strike=False, render_font='Times New Roman'):
        """
            Rich text render
            :param render_font:
            :param text_variable:
            :param text_content
            :param render_underlined:
            :param render_bold: False
            :param render_italic: False
            :param render_strike: False
            :param render_color: '#000000'
            :param render_size: 14
            :return: self
        """

        rich_text = RichText(text_content, italic=render_italic,
                             bold=render_bold, strike=render_strike,
                             color=render_color, size=render_size, font=render_font, underline=render_underlined)

        context = {text_variable: rich_text}

        self.document = DocxTemplate(self.path_to_sample)
        self.document = DocxTemplate(self.path_to_sample)
        self.document.render(context)

        # return self

    def save(self):
        """
            Multiple render and file saver
            :return:
        """

        self.document.save(self.last_file_path)
        return self.last_file_path

    def check(self, document_context_kwargs):
        """
        checks document keywords
        asserts: There is no param in your dict
        :return True
        """
        for key_val in self.attributes:
            assert key_val in document_context_kwargs, \
                f'There is no "{key_val}" param \ in your dict: {document_context_kwargs} \n{self.attributes}'

        return True

    @staticmethod
    def preprocess_full_name(full_name):
        """
        Process full_name: Abs Abs Abs into format Abs A. A.
        :param full_name - array with len 2 or 3
        :return full_name - processed name
        """
        full_name = ' '.join([full_name.split()[0], *[initial[0] + '.' for initial in full_name.split()[1:]]])
        return full_name

    @staticmethod
    def preprocess_date(date):
        """
        Process date from dd.mm.yyyy to dd.mm.yy
        :param date:
        :return: date
        """

        (dd, mm, yy) = date.split('.')
        return '.'.join([dd, mm, yy[-2:]])

    @staticmethod
    def preprocess_yes_no(y_n):
        return "Имеются" if y_n.strip().lower() == "да" else 'Отсутствуют'

    def preprocess_path_to_save(self, full_name):
        """
        adds full_name.docx to self.path_to_save
        :param: Full Name
        :return: full name -> path_to_save/ApplicationType_Full_Name.docx
        """
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

        full_name = '_'.join(full_name.split())
        application_type = self.__name__()

        file_path = application_type + "_" + date + "_" + full_name + '.docx'

        return os.path.join(self.path_to_save, file_path)

    def send_gmail(self, address, body_msg=''):
        """sends emails to the specified address
        :param body_msg: message with document
        :param address: recipient's address"""

        gs = GmailSender()
        gs.send_gmail(recipient=address, body=body_msg,
                      file_path=self.last_file_path)


if __name__ == '__main__':
    print(AbstractDocument.preprocess_date('16.10.2001'))
    print(AbstractDocument('DocSample/relocation_sample.docx', 'DocBase').preprocess_path_to_save(
        'Полукаров Иван Сергеевич'))
