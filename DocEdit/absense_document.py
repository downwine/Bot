from DocEdit.abstract_document import AbstractDocument
import os


class AbsenceDocument(AbstractDocument):
    def __init__(self, path_to_sample='DocEdit/DocSample/abscence_sample.docx', path_to_save='DocEdit/DocBase'):
        # list of variables in file
        self.attributes = ["full_name", "room_number", "phone_number", "period_from", "period_to",
                           "reason", 'current_date']
        self.__docname__ = 'НаВременноеОтсутствие'
        super().__init__(path_to_sample, path_to_save)


if __name__ == '__main__':
    test_dict = {"full_name": 'Полукаров Иван Cергеевич',
                 "room_number": 123,
                 'phone_number': 88005553534,
                 "period_from": '12.12.2020',
                 "period_to": '12.12.2021',
                 "reason": "тем, что я умер",
                 'current_date': '12.12.2020'}

    document = AbsenceDocument()
    document.write_usual(test_dict)
    document.send_document()