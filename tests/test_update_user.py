import pytest
import allure
from faker import Faker
from enums.age_enums import Ages

static_surname = Faker().last_name()
static_name = Faker().first_name()
static_age = Faker().random_int(min=Ages.MIN_AGE.value, max=Ages.MAX_AGE.value)


@pytest.mark.parametrize("user_data, extra_field, expected_status", [
    ({}, {"name": static_name}, "success"),
    ({}, {"surname": static_surname}, "success"),
    ({}, {"age": static_age}, "success"),

], ids=["обновление имени", "обновление фамилии", "обновление возраста"], indirect=True)
def test_success_update_of_each_field(ws_connection, select_user, add_user, user_data, extra_field, delete_user,
                                      parse_response, update_user, expected_status):
    """
          Успешное обновление каждого из полей юзера
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]

    with allure.step(f"Updating user with data: {user_data}"):
        print("user_data равна", user_data)
        user_data.update(extra_field)
        print("user_data равна", user_data)
        update_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        assert response_data.method == "update"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]


def test_failure_update_absent_user(ws_connection, select_user, add_user, user_data,
                                    parse_response, update_user):
    """
          Неуспешное обновление отсутствующего юзера
          """

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert response_data.users is None

    with allure.step(f"Updating user with data: {user_data}"):
        update_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == "failure"
        assert response_data.method == "update"
        assert response_data.id == user_data["id"]
