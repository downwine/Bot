from Gmail.GmailSender import GmailSender


class Photo:
    def __init__(self, path_to_photo):
        self.path_to_photo = path_to_photo

    def send_photo(self, address, body_msg='Здесь должно быть чье-то имя(параметр body_mgs)'):
        """sends emails to the specified address
        :param body_msg: message with document
        :param address: recipient's address"""

        gs = GmailSender()
        gs.send_photo(recipient=address,
                      file_path=self.path_to_photo,
                      body=body_msg)


if __name__ == '__main__':
    gs = GmailSender()
    p = Photo('C:/Users/vanis/PycharmProjects/Bot/DocEdit/DocSample/some_cat.jpg')
    p.send_photo('polukarov.i@sch009.net')