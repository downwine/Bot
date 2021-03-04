from docxtpl import DocxTemplate
from docxtpl import RichText
import os


class AbstractDocument:
    def __init__(self):
        self.template_path = None  #
        self.document = None

    def write_usual(self, **document_context_kwargs):
        """
            Multiple render and file saver
            :param document_context_kwargs - dict of {{ vars }} and their values
            :return:
        """

        self.document = DocxTemplate(self.template_path)  # reading document with __init__ path param
        self.document.render(document_context_kwargs)
        # self.document.save(path_to_save_file)

    def save(self, path_to_save_file='DefaultTest.docx'):
        """
            Multiple render and file saver
            :param path_to_save_file: Default: DefaultTest.docx - path to file
            :return:
        """

        self.document.save(path_to_save_file)

    def write_rich(self, text_content, italic=False, color='#000000'):
        """
            Rich text render
            :param text_content
            :param rich_text_kwargs - dict of {{ vars }} and their values
            :return:
        """

        # rt = RichText(text_content, *rich_text_kwargs)
