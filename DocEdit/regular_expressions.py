import re


def mobile_valid_check(phone_number):
    """
    valid phone check
    :param: phone_number: phone_number
    :return: bool: is number valid
    """

    pattern = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
    letters = re.compile(r'[^0-9-+() ]')

    if letters.search(phone_number):
        return False

    phone_number = phone_number.replace(' ', '')
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(')', '')
    phone_number = phone_number.replace('(', '')

    return True if pattern.search(phone_number) else False


def reformat_mobile(phone_number):
    """
        valid phone check
        :param: phone_number: phone_number
        :return: processed phone number with format xxx.xxx.xx.xx
    """

    if not mobile_valid_check(phone_number):
        return None

    phone_number = phone_number.replace(' ', '')
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(')', '')
    phone_number = phone_number.replace('(', '')
    phone_number = phone_number.replace('+', '')

    return phone_number


def full_name_check(full_name):
    """
        valid phone check
        :param: full_name: string with surname, name, (patronymic)
        :return: bool: is full_name valid
    """

    full_name = full_name.lstrip(' ')
    full_name = full_name.rstrip(' ')

    pattern = re.compile(r'[^a-zA-Zа-яА-Я ]')

    if pattern.search(full_name):
        return False

    return len(full_name.split(' ')) >= 2


def full_name_processing(full_name):
    """
        valid phone check
        :param: full_name: string with surname, name, (patronymic)
        :return: None if not full_name_check else processed full_name
    """

    if not full_name_check(full_name):
        return None

    full_name = full_name.lower()
    full_name = full_name.title()

    return full_name
