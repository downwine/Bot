from DocEdit.abstract_document import AbstractDocument
import os


class RelocationDocument(AbstractDocument):
    def __init__(self, path_to_sample='DocSample/relocation_sample.docx', path_to_save='DocBase'):
        # list of variables in file
        self.attributes = ["full_name", "room_number", "phone_number", "room_to", "room_from",
                           "reason", "academ_debt", "reprimands", "neighbors"]

        self.__docname__ = 'НаПереселение'
        super().__init__(path_to_sample, path_to_save)

    def preprocess_dict(self, document_context_kwargs):
        document_context_kwargs['academ_debt'] = self.preprocess_yes_no(document_context_kwargs['academ_debt'])
        document_context_kwargs['reprimands'] = self.preprocess_yes_no(document_context_kwargs['reprimands'])
        # document_context_kwargs['neighbors'] = self.preprocess_neighbors(document_context_kwargs['neighbors'])
        super().preprocess_dict(document_context_kwargs)


if __name__ == '__main__':
    test_dict = {
        "full_name": 'Полукаров Иван Cергеевич',
        "room_number": 123,
        'phone_number': 88005553534,
        "room_to": 124,
        'room_from': 123,
        "reason": "потому что я заебался писать код",
        "academ_debt": "ДА",
        "reprimands": "НЕТ",
        "current_date": "15.10.2021",
        "neighbors": "Кто То СОтч1еством, КтоТоБез Отчества"
    }

    document = RelocationDocument()
    document.write_usual(test_dict)
    document.send_gmail(address='polukarov.i@sch2009.net', body_msg='Прив КДЧД')
