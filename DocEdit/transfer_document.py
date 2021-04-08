from DocEdit.abstract_document import AbstractDocument
import os


class TransferDocument(AbstractDocument):
    def __init__(self, path_to_sample='DocEdit/DocSample/transfer_sample.docx', path_to_save='DocEdit/DocBase'):
        # list of variables in file
        self.attributes = ["full_name", "room_number", "phone_number", "date_of_moving", "in_or_out",
                           "list_of_items", "neighbors", 'current_date']

        self.__docname__ = 'НаПроносВещей'
        super().__init__(path_to_sample, path_to_save)

    def preprocess_dict(self, document_context_kwargs):
        document_context_kwargs['in_or_out'] = document_context_kwargs['in_or_out'].lower()
        super().preprocess_dict(document_context_kwargs)


if __name__ == "__main__":
    test_dict = {"full_name": "Полукаров Иван Сернеевич",
                 "room_number": 123,
                 "phone_number": 88005553535,
                 "date_of_moving": '16.20.2020',
                 "in_or_out": "ВНОС",
                 "list_of_items": 'укроп, кошачья жопа, двадцать пять картошин, ведро воды и хуй туды, охапку дров',
                 "neighbors": "Рикардо Милос Сльбертович, Жмышенко Валерий Альбертович",
                 'current_date': '25.12.2002'}

    document = TransferDocument()
    document.write_usual(test_dict)
    document.send_gmail(address='polukarov.i@sch2009.net', body_msg='Прив КДЧД')