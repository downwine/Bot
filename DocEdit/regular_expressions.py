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
        print(letters.search(phone_number))
        return False

    phone_number = phone_number.replace(' ', '')
    phone_number = phone_number.replace('-', '')
    phone_number = phone_number.replace(')', '')
    phone_number = phone_number.replace('(', '')

    return True if pattern.search(phone_number) else False


if __name__ == '__main__':
    print(mobile_valid_check('+7 925 -914 65 44'))
    print(mobile_valid_check('40 925 -914 65 44'))
    print(mobile_valid_check('+8 (925) -914 65 44'))
    print(mobile_valid_check(' 925 -914 65 44'))
    print(mobile_valid_check('+7 925 -914 65 '))
    print(mobile_valid_check('925 -914f 65 44'))
    print(mobile_valid_check('925 -914? 65 44'))
