def search_in_table(row_max, search_text, sheet_active, column):
    """
    Функция для поиска данных в указанном столбце
    :param row_max:
    :param search_text:
    :param sheet_active:
    :param column:
    :return:
    """
    from openpyxl.utils import get_column_letter
    import re
    row_min = 1  # Переменная, отвечающая за номер строки
    column = column  # Переменная, отвечающая за номер столбца
    m = []

    search_text = str(search_text)
    row_min_min = row_min
    row_max_max = row_max
    while row_min_min <= row_max_max:
        row_min_min = str(row_min_min)

        word_column = get_column_letter(column)
        word_column = str(word_column)
        word_cell = word_column + row_min_min

        data_from_cell = sheet_active[word_cell].value
        data_from_cell = str(data_from_cell)
        # print(data_from_cell)
        regular = search_text
        result = re.findall(regular, data_from_cell)
        row_min_min = int(row_min_min)
        row_min_min = row_min_min + 1
        if len(result) > 0:
            m.append(word_cell)
    return m


def search_id(search_text):
    import openpyxl

    path_to_file = 'Список проживающих.xlsx'
    wb = openpyxl.load_workbook(path_to_file)  # Грузим наш список
    sheet_active = wb.active  # Начинаем работать с файлом
    row_max = sheet_active.max_row  # Получаем количество строк
    # print(type(row_max))
    word_cell = search_in_table(row_max, search_text, sheet_active, 2)

    if not word_cell:
        return None
    else:
        b = sheet_active.cell(row=int(word_cell[0][1:]), column=1).value
        return b


# print(search_id(207826855))

def search_name(search_text):
    import openpyxl

    path_to_file = 'Список проживающих.xlsx'
    wb = openpyxl.load_workbook(path_to_file)  # Грузим наш список
    sheet_active = wb.active  # Начинаем работать с файлом
    row_max = sheet_active.max_row  # Получаем количество строк
    # print(type(row_max))
    word_cell = search_in_table(row_max, search_text, sheet_active, 1)

    if not word_cell:
        return None
    else:
        b = sheet_active.cell(row=int(word_cell[0][1:]), column=2).value
        return b


def duty_hours_today(flags):
    import datetime
    import openpyxl

    current_datetime = datetime.datetime.now()
    if current_datetime.hour == 2:
        b = []
        for i in 2, 3, 4, 5, 6, 7, 9:
            path_to_file = f'График дежурств {i} этаж.xlsx'
            try:
                wb = openpyxl.load_workbook(path_to_file)  # Грузим наш график
            except:
                print(f'График дежурств {i} этаж.xlsx отсутствует')
                continue
            sheet_active = wb.active  # Начинаем работать с файлом
            search_text = sheet_active.cell(row=current_datetime.day + 3, column=1).value

            path_to_file = 'Список проживающих.xlsx'
            wb = openpyxl.load_workbook(path_to_file)  # Грузим наш список
            sheet_active = wb.active  # Начинаем работать с файлом
            row_max = sheet_active.max_row  # Получаем количество строк
            word_cell = search_in_table(row_max, search_text, sheet_active, 1)
            # print(word_cell)
            if not word_cell:
                b.append(None)
            else:
                b.append(sheet_active.cell(row=int(word_cell[0][1:]), column=2).value)

        notify_cleaners(b, flags)


def notify_cleaners(id_of_cleaners, flags):
    import vk_api
    from our_token import token
    from filling_docs import send_msg_without_keyboard

    i = 0
    vk_session = vk_api.VkApi(token=token)
    for idd in id_of_cleaners:
        if vk_session.method("messages.isMessagesFromGroupAllowed",
                             {"group_id": 202823499, "user_id": idd})["is_allowed"]:
            if not flags[i]:
                send_msg_without_keyboard(idd, "Ты сегодня дежурный! Не забудь прибраться ;)")
                flags[i] = True
                i += 1


# print(duty_hours_today())


def duty_hours_when(search_text):
    import openpyxl
    word_cell = []
    b = search_id(search_text)
    if not b:
        return None
    p = b.split(" ")
    search_text = p[0] + " " + p[1][:1]
    for i in 2, 3, 4, 5, 6, 7, 9:
        path_to_file = f'График дежурств {i} этаж.xlsx'
        try:
            wb = openpyxl.load_workbook(path_to_file)  # Грузим наш график
        except:
            print(f'График дежурств {i} этаж.xlsx отсутствует')
            continue
        sheet_active = wb.active  # Начинаем работать с файлом
        row_max = sheet_active.max_row  # Получаем количество строк
        word_cell_test = search_in_table(row_max, search_text, sheet_active, 1)
        if not word_cell_test:
            search_text = p[0]
            word_cell_test = search_in_table(row_max, search_text, sheet_active, 1)
        if word_cell_test:
            word_cell = word_cell_test

    s = []
    if not word_cell:
        return None
    else:
        for i in range(len(word_cell)):
            s.append(int(word_cell[i][1:]) - 3)
        return s


# print(duty_hours_when(114075926))


def delete_row(name):
    import openpyxl

    path_to_file = 'Список проживающих.xlsx'
    wb = openpyxl.load_workbook(path_to_file)  # Грузим наш список
    sheet_active = wb.active  # Начинаем работать с файлом
    row_max = sheet_active.max_row  # Получаем количество строк
    word_cell = search_in_table(row_max, name, sheet_active, 1)
    if not word_cell:
        return None
    else:
        b = word_cell[0][1:]
        sheet_active.delete_rows(int(b))
        wb.save('Список проживающих.xlsx')


# delete_row('Михайлов Артем Алексеевич')


def add_name(name, id_number):
    import openpyxl

    path_to_file = 'Список проживающих.xlsx'
    wb = openpyxl.load_workbook(path_to_file)  # Грузим наш список
    sheet_active = wb.active  # Начинаем работать с файлом
    row_max = sheet_active.max_row  # Получаем количество строк
    first_cell = "A" + str(row_max + 1)
    second_cell = "B" + str(row_max + 1)
    sheet_active[first_cell].value = name
    sheet_active[second_cell].value = id_number
    wb.save('Список проживающих.xlsx')

# add_name('Катя', 345)
