import allure
from faker import Faker
from enums.error_message_enums import ReasonErrorMessages

from utils.helping_methods import parse_response


# TO_DO
# def test_delete_user_with_other_fields_in_request


# @pytest.mark.skip
def test_success_delete_user(ws_connection, select_user, add_user, user_data, delete_user):
    """
          Успешное удаление юзера
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

    with allure.step(f"Deleting user with data: {user_data}"):
        current_id = Faker().uuid4()
        delete_user({"phone": user_data["phone"],
                     "id": current_id})
        response_data = parse_response(ws_connection.recv())
        assert response_data.id == current_id
        assert response_data.method == "delete"
        assert response_data.status == "success"

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert response_data.users is None


# @pytest.mark.skip
def test_failure_delete_non_existing_user(ws_connection, select_user, user_data, add_user, delete_user):
    """
          Реквест на удаление без телефона
          """
    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert response_data.users is None

    with allure.step(f"Deleting user with data: {user_data}"):
        current_id = Faker().uuid4()
        delete_user({"id": current_id,
                     "phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())
        assert response_data.id == current_id
        assert response_data.method == "delete"
        assert response_data.status == "failure"


# @pytest.mark.skip
def test_failure_delete_without_phone_field(ws_connection, select_user, add_user, delete_user):
    """
          Удаление  юзера без поля phone
          """

    with allure.step(f"Deleting user with data: no phone"):
        current_id = Faker().uuid4()
        delete_user({"id": current_id})
        response_data = parse_response(ws_connection.recv())
        assert response_data.id == current_id
        assert response_data.method == "delete"
        assert response_data.status == "failure"
        assert response_data.reason == ReasonErrorMessages.KEY_PHONE_NOT_FOUND.value


# @pytest.mark.skip
def test_failure_delete_with_space_in_phone_field(ws_connection, select_user, delete_user):
    """
          Удаление юзера c пробелом в поле phone
          """

    with allure.step(f"Deleting user with data: no phone"):
        current_id = Faker().uuid4()
        delete_user({"id": current_id,
                     "phone": " "})
        response_data = parse_response(ws_connection.recv())
        assert response_data.id == current_id
        assert response_data.method == "delete"
        assert response_data.status == "failure"


# @pytest.mark.skip
def test_failure_delete_with_empty_value_in_phone_field(ws_connection, select_user, delete_user):
    """
          Удаление юзера c пустым полем phone
          """

    with allure.step(f"Deleting user with data: no phone"):
        current_id = Faker().uuid4()
        delete_user({"id": current_id,
                     "phone": ""})
        response_data = parse_response(ws_connection.recv())
        assert response_data.id == current_id
        assert response_data.method == "delete"
        assert response_data.status == "failure"
