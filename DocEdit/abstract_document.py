from docxtpl import DocxTemplate
from docxtpl import RichText


class AbstractDocument:
    def __init__(self):
        if __name__ == "__main__":
            print(__name__)
            self.template_path = 'relocation_sample.docx'
            self.document = DocxTemplate(self.template_path)
        else:
            self.template_path = None
            self.document = None

    def write_usual(self, **document_context_kwargs):
        """
            Multiple render and file saver
            :param document_context_kwargs - dict of {{ vars }} and their values
            :return: self
        """

        # self.document = DocxTemplate(self.template_path)  # reading document with __init__ path param
        self.document.render(document_context_kwargs)
        # self.document.save(path_to_save_file)

        # return self

    def write_rich(self, text_variable, text_content, render_italic=False,
                   render_underlined=False, render_bold=False, render_color='#000000',
                   render_size=24, render_strike=False, render_font='Times New Roman', underline=False):
        """
            Rich text render
            :param underline:
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
                             color=render_color, size=render_size, font=render_font, underline=underline)

        context = {text_variable: rich_text}
        self.document.render(context)

        # return self

    def save(self, path_to_save_file='DefaultTest.docx'):
        """
            Multiple render and file saver
            :param path_to_save_file: Default: DefaultTest.docx - path to file
            :return:
        """

        self.document.save(path_to_save_file)


if __name__ == '__main__':
    print('abstract_document.py')
    ad = AbstractDocument()
    ad.write_rich(text_variable='full_name', text_content='Полукаров Иван Сергеевич', underline=True)
    ad.save()
