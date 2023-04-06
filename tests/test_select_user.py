import pytest
import allure
from faker import Faker

# TO_DO
# def test_failure_select_absent_user

static_surname = Faker().last_name()
static_name = Faker().name()


# @pytest.mark.skip
def test_success_select_user_by_phone(ws_connection, select_user, add_user, user_data, delete_user, parse_response):
    """
          Успешное получение юзера по номеру телефона
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


# @pytest.mark.skip
def test_success_select_user_by_name(ws_connection, select_user, add_user, user_data, delete_user, parse_response):
    """
          Успешное получение юзера по имени
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"name": user_data["name"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]


# @pytest.mark.skip
def test_success_select_user_by_surname(ws_connection, select_user, add_user, user_data, delete_user, parse_response):
    """
          Успешное получение юзера по фамилии
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"surname": user_data["surname"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]


@pytest.mark.skip  # ПРОПУЩЕН, Т.К. ДЕФФЕКТ БЛОКЕР
def test_failure_select_without_fields(ws_connection, select_user, add_user, user_data, delete_user, parse_response):
    """
          Получение юзера без других полей
          """

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]


# @pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"name": "", "fields_to_exclude": ["surname", "age", "phone"]}, "failure"),
    ({"surname": "", "fields_to_exclude": ["name", "age", "phone"]}, "failure"),
    ({"phone": "", "fields_to_exclude": ["surname", "age", "name"]}, "failure")
], ids=["пустой name", "пустой surname", "пустой phone"], indirect=True)
def test_select_user_with_empty_value_in_one_field(ws_connection, select_user, add_user, user_data, delete_user,
                                                   expected_status, parse_response):
    """
          Получение пользователей с одним полем без значения
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]


# @pytest.mark.skip
@pytest.mark.parametrize("get_user_data_list", [{"user1": {"surname": static_surname},
                                                 "user2": {"surname": static_surname}}],
                         ids=["two_users_one_phone"], indirect=True)
def test_select_two_users_with_same_surname(ws_connection, select_user, get_user_data_list, add_user, parse_response):
    """
          Получение двух юзеров с одинаковoй фамилией
          """
    first_user_data = get_user_data_list[0]
    second_user_data = get_user_data_list[1]

    with allure.step(f"Adding first user with data: {first_user_data}"):
        add_user(first_user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == first_user_data["id"]

    with allure.step(f"Adding second user with data: {second_user_data}"):
        add_user(second_user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == second_user_data["id"]

    with allure.step(f"Selecting user with data: {first_user_data}"):
        select_user({"surname": first_user_data["surname"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 2

        for user in response_data.users:
            assert user.name == get_user_data_list[user]["name"]
            assert user.surname == first_user_data[user]["surname"]
            assert user.phone == first_user_data[user]["phone"]
            assert user.age == first_user_data[user]["age"]


@pytest.mark.parametrize("get_user_data_list", [{"user1": {"name": static_name},
                                                 "user2": {"name": static_name}}],
                         ids=["two_users_one_phone"], indirect=True)
def test_select_two_users_with_same_name(ws_connection, select_user, get_user_data_list, add_user, parse_response):
    """
          Получение двух юзеров с одинаковым именем
          """
    first_user_data = get_user_data_list[0]
    second_user_data = get_user_data_list[1]

    with allure.step(f"Adding first user with data: {first_user_data}"):
        add_user(first_user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == first_user_data["id"]

    with allure.step(f"Adding second user with data: {second_user_data}"):
        add_user(second_user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == second_user_data["id"]

    with allure.step(f"Selecting user with data: {first_user_data}"):
        select_user({"name": first_user_data["name"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 2

        first_user = response_data.users[0]
        second_user = response_data.users[1]

        assert first_user.name == first_user_data["name"]
        assert first_user.surname == first_user_data["surname"]
        assert first_user.phone == first_user_data["phone"]
        assert first_user.age == first_user_data["age"]

        assert second_user.name == second_user_data["name"]
        assert second_user.surname == second_user_data["surname"]
        assert second_user.phone == second_user_data["phone"]
        assert second_user.age == second_user_data["age"]
