import string
import random
from faker import Faker
from enums.name_enums import LengthsOfNames

normal_name_length = LengthsOfNames.NORMAL_NAME_LENGTH.value
max_name_length = LengthsOfNames.MAX_NAME_LENGTH.value
min_name_length = LengthsOfNames.MIN_NAME_LENGTH.value


def cyrillic_string():
    """Генерация строки на кириллице заданной длины"""
    cyrillic_chars = [chr(char) for char in range(1040, 1104)]
    return ''.join(random.choice(cyrillic_chars) for _ in range(normal_name_length))


def latin_string():
    """Генерация строки на латинице заданной длины"""
    latin_chars = string.ascii_letters
    return ''.join(random.choice(latin_chars) for _ in range(normal_name_length))


def alphanumeric_string():
    """Генерация строки на латинице, включающей цифры"""
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(normal_name_length))


def special_string():
    """Генерация строки, включающей специальные символы"""
    special_chars = string.printable
    return ''.join(random.choice(special_chars) for _ in range(normal_name_length))


def mixed_alphabet_string():
    alphabet = string.ascii_letters + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    return ''.join(random.choice(alphabet) for _ in range(normal_name_length))


def long_string():
    """Генерация очень длинной строки"""
    return 'a' * (max_name_length + 1)


def short_string():
    """Генерация очень длинной строки"""
    if min_name_length >= 1:
        return 'a' * (min_name_length - 1)
    else:
        return ''


def max_string():
    """Генерация очень длинной строки"""
    return 'a' * (max_name_length)


def min_string():
    """Генерация очень длинной строки"""
    return 'a' * (min_name_length)
