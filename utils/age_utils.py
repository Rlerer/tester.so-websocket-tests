import random
from enums.age_enums import Ages

min_age = Ages.MIN_AGE.value
max_age = Ages.MAX_AGE.value


def str_age():
    """Генерация случайного возраста от 1 до 100 в строке"""
    return str(random.randint(min_age, max_age))


def int_age():
    """Генерация случайного возраста от 1 до 100"""
    return random.randint(min_age, max_age)


def float_age():
    """Генерация случайного возраста с плавающей точкой от 1 до 100"""
    return round(random.uniform(min_age, max_age), 2)


def negative_age():
    """Генерация случайного отрицательного возраста от -100 до -1"""
    return random.randint(min_age, max_age) * -1


def maximum_age():
    """Генерация случайного отрицательного возраста от -100 до -1"""
    return max_age


def minimum_age():
    """Генерация случайного отрицательного возраста от -100 до -1"""
    return min_age


def underqualified_age():
    """Генерация случайного отрицательного возраста от -100 до -1"""
    return min_age - 1


def overqualified_age():
    """Генерация случайного отрицательного возраста от -100 до -1"""
    return max_age + 1
