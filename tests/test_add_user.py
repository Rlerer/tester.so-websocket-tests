import pytest
import allure
from enums.error_message_enums import ReasonErrorMessages
from conftest import static_surname


# @pytest.mark.new
# @pytest.mark.parametrize("user_data, expected_status", [
#     ({"fields_to_exclude": ["name"]}, "failure"),
#     ({"fields_to_exclude": ["surname"]}, "failure"),
#     ({"fields_to_exclude": ["phone"]}, "failure"),
#     ({"fields_to_exclude": ["age"]}, "failure"),
# ], ids=[ "без name", "без surname", "без phone", "без age"], indirect=True)
# def test_delete_user_12(ws_connection, add_user, user_data, delete_user, expected_status, parse_response):
#     """
#          добавление пользователей с одним отстутствующим полем method или id
#           """
#     with allure.step(f"Adding user with data: {user_data}"):
#         add_user(user_data, expected_status)
#         response = ws_connection.recv()
#         response_data = parse_response(response)
#         request_data = user_data
#         print('user_data вот такая нахуй', user_data)
#         assert response_data.status == expected_status
#         assert response_data.method == "add"
#         assert response_data.id == request_data["id"]


# TO_DO
# KEY_ID_NOT_FOUND = "[json.exception.out_of_range.403] key 'id' not found"
# KEY_METHOD_NOT_FOUND = "[json.exception.out_of_range.403] key 'method' not found"


@pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status, expected_reason", [
    ({"fields_to_exclude": ["name"]}, "failure", ReasonErrorMessages.KEY_NAME_NOT_FOUND.value),
    ({"fields_to_exclude": ["surname"]}, "failure", ReasonErrorMessages.KEY_SURNAME_NOT_FOUND.value),
    ({"fields_to_exclude": ["phone"]}, "failure", ReasonErrorMessages.KEY_PHONE_NOT_FOUND.value),
    ({"fields_to_exclude": ["age"]}, "failure", ReasonErrorMessages.KEY_AGE_NOT_FOUND.value),
], ids=["без name", "без surname", "без phone", "без age"], indirect=True)
def test_add_user_without_one_field(ws_connection, add_user, user_data, select_user, expected_status, parse_response,
                                    expected_reason):
    """
         Добавление пользователей с одним отстутствующим полем запроса
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, expected_status)
        response_data = parse_response(ws_connection.recv())

        assert response_data.id == user_data["id"]
        assert response_data.method == "add"
        assert response_data.status == expected_status
        assert response_data.reason == expected_reason

    with allure.step(f"Selecting user with data: {user_data}"):
        if "phone" in user_data:
            select_user({"phone": user_data["phone"]}, expected_status)
        else:
            select_user({"surname": user_data["surname"]}, expected_status)

        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == expected_status
        assert response_data.users is None


@pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"id": " "}, "failure"),
    ({"name": " "}, "failure"),
    ({"surname": " "}, "failure"),
    ({"phone": " "}, "failure"),
    ({"age": " "}, "failure"),
], ids=["пустой id", "пустой name", "пустой surname", "пустой phone", "пустой age"], indirect=True)
def test_add_user_with_space_in_one_field(ws_connection, select_user, add_user, user_data, delete_user, expected_status,
                                          parse_response):
    """
         Добавление пользователей с пробелом в значении одного из полей
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, expected_status)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        if "phone" in user_data:
            select_user({"phone": user_data["phone"]}, expected_status)
        else:
            select_user({"surname": user_data["surname"]}, expected_status)

        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == expected_status
        assert response_data.users is None


@pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"id": ""}, "failure"),
    ({"name": ""}, "failure"),
    ({"surname": ""}, "failure"),
    ({"phone": ""}, "failure"),
    ({"age": ""}, "failure"),
], ids=["пустой id", "пустой name", "пустой surname", "пустой phone", "пустой age"], indirect=True)
def test_add_user_with_empty_value_in_one_field(ws_connection, select_user, add_user, user_data, delete_user,
                                                expected_status, parse_response):
    """
          Добавление пользователей с одним полем без значения
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, expected_status)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        if "phone" in user_data:
            select_user({"phone": user_data["phone"]}, expected_status)
        else:
            select_user({"surname": user_data["surname"]}, expected_status)

        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == expected_status
        assert response_data.users is None


def test_success_add_user(ws_connection, select_user, add_user, user_data, delete_user, parse_response):
    """
          Успешное добавление юзера
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
        print('user_data вот такая нахуй', user_data)

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]
