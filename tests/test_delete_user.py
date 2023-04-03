import pytest
import allure
from faker import Faker

static_surname = Faker().last_name()


@pytest.mark.delete
@pytest.mark.old
@pytest.mark.parametrize("user_data", [
    {},
    {"name": "Иван", "surname": "Говнов"},
    {"name": "Джизас", "age": 33},
    {"name": "Джизас", "age": 33}
    # {"fields_to_exclude": ["age"]}

], ids=["test_case_1", "test_case_2", "test_case_3", "cock_lover"], indirect=True)
# @pytest.mark.parametrize("expected_status", [
#     "success",
#     "success",
#     "success",
#     "success"
# ], ids=["test_case_1", "test_case_2", "test_case_3", "cock_lover"])
def test_delete_user_success(add_user, user_data, delete_user):
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, "success")
        delete_user(user_data, "success")


@pytest.mark.old
@pytest.mark.parametrize("user_data, expected_status", [
    ({"name": "Иван", "surname": "Говнов"}, "success"),
    ({"name": "Джизас", "age": 33}, "fasdlure")
], ids=["test_case_1", "test_case_2"], indirect=True)
def test_delete_user_success(add_user, user_data, delete_user, expected_status):
    """
        удаляем челов с кастомным статусом
        """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, expected_status)
        delete_user(user_data, expected_status)


@pytest.mark.old
@pytest.mark.parametrize("user_data, expected_status", [
    ({"name": "Иван", "surname": static_surname}, "failure"),
    ({"surname": static_surname}, "failure")
], ids=["test_case_1","срань людей"], indirect=True)
def test_delete_user_12(ws_connection, add_user, user_data, delete_user, expected_status, parse_response):
    """
        удаляем челов с кастомным статусом
        """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, expected_status)
        response = ws_connection.recv()
        response_data = parse_response(response)
        request_data = user_data
        print('user_data вот такая нахуй', user_data)
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == request_data["id"]

    with allure.step(f"Deleting user with data: {user_data}"):
        delete_user(user_data, expected_status)
        response = ws_connection.recv()
        response_data = parse_response(response)
        print('user_data вот такая нахуй', user_data)
        assert response_data.status == expected_status
        assert response_data.method == "delete"
        assert response_data.id == request_data["id"]


@pytest.mark.hmm
@pytest.mark.parametrize("get_user_data_list", [{"user1": {"name": "John", "surname": static_surname, "age": 30},
                                                  "user2": {"name": "Jane", "surname": static_surname, "age": 25}}], indirect=True)
def test_delete_user_2324(ws_connection, add_user, delete_user, parse_response, get_user_data_list):
    """
        удаляем челов с кастомным статусом
        """
    with allure.step(f"Adding user with data: {get_user_data_list[0]}"):
        add_user(get_user_data_list[0], "success")
        response = ws_connection.recv()
        response_data = parse_response(response)
        request_data = get_user_data_list[0]
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == request_data["id"]

    with allure.step(f"Deleting user with data: {get_user_data_list[0]}"):
        delete_user(get_user_data_list[0], "success")
        response = ws_connection.recv()
        response_data = parse_response(response)
        assert response_data.status == "success"
        assert response_data.method == "delete"
        assert response_data.id == request_data["id"]
