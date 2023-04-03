import pytest
import websocket
import json
import random
import string
import allure

@pytest.mark.old
def test_add_user_success1(add_user, user_data):
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, "success")
    print(f"User data: {user_data}")


@pytest.mark.old
@pytest.mark.parametrize("user_data", [
    {},
    {"name": "Иван", "surname": "Говнов"},
    {"name": "Jane", "age": 30},
], indirect=True)

def test_add_user_success(user_data, add_user):
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, "success")
    print(f"User data: {user_data}")


@pytest.mark.old
@pytest.mark.parametrize("user_data", [
    {"surname": "Smith", "phone": "+3443467490"}, #один и тот же номер, пофикшу
    {"name": "Bob", "fields_to_exclude": ["surname"]}, #нет поля
    {"fields_to_exclude": ["surname","name"]},  # нет поля
    {"fields_to_exclude": ["age"]},  # нет поля
], indirect=True)

def test_add_user_failure(user_data, add_user):
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, "failure")
    print(f"User data: {user_data}")
