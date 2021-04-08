from DocEdit.abstract_document import AbstractDocument
import os


class GuestDocument(AbstractDocument):
    def __init__(self, path_to_sample='DocSample/guest_sample.docx', path_to_save='DocBase'):
        # list of variables in file
        self.attributes = ["full_name", "room_number", "phone_number", "guest_name", "invitation_room",
                           "day_of_visit", "time_from", "current_date", "time_to", "neighbors"]

        super().__init__(path_to_sample, path_to_save)
        self.__docname__ = 'НаПроходГостя'

if __name__ == '__main__':
    test_dict = {
        "full_name": 'Полукаров Иван Сергеевич',
        "room_number": 123,
        "phone_number": 88005553535,
        "guest_name": "Рикардо Милос Альбертович",
        "invitation_room": 213,
        "day_of_visit": "16.10.2021",
        "time_from": "16.00",
        "time_to": "17.00",
        "current_date": "15.10.2021",
        "neighbors": "Кто То СОтчеством, КтоТоБез Отчества"
    }

    #print(test_dict)
    document = GuestDocument()
    document.write_usual(test_dict)
