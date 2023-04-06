import pytest
import allure
from faker import Faker
from enums.error_message_enums import ReasonErrorMessages
from utils import name_utils, age_utils

# TO_DO
# def test_add_users_with_different_types_of_phone
# def test_use_several_methods_at_once
# KEY_ID_NOT_FOUND = "[json.exception.out_of_range.403] key 'id' not found"
# KEY_METHOD_NOT_FOUND = "[json.exception.out_of_range.403] key 'method' not found"

static_phone = Faker().phone_number()


# было бы неплохо, конечно

# def check_user_data(user_data, expected_status, ws_connection, select_user, parse_response):
#     select_user({"phone": user_data["phone"]})
#     response_data = parse_response(ws_connection.recv())
#
#     assert response_data.method == "select"
#     assert response_data.status == expected_status
#
#     if expected_status == "success":
#         assert len(response_data.users) == 1
#
#         current_user = response_data.users[0]
#
#         assert current_user.name == user_data["name"]
#         assert current_user.surname == user_data["surname"]
#         assert current_user.phone == user_data["phone"]
#         assert current_user.age == user_data["age"]


# @pytest.mark.skip
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
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.id == user_data["id"]
        assert response_data.method == "add"
        assert response_data.status == expected_status
        assert response_data.reason == expected_reason

    with allure.step(f"Selecting user with data: {user_data}"):
        if "phone" in user_data:
            select_user({"phone": user_data["phone"]})
        else:
            select_user({"surname": user_data["surname"]})

        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == expected_status
        assert response_data.users is None


# @pytest.mark.skip
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
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        if "phone" in user_data:
            select_user({"phone": user_data["phone"]})
        else:
            select_user({"surname": user_data["surname"]})

        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == expected_status
        assert response_data.users is None


# @pytest.mark.skip
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
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        if "phone" in user_data:
            select_user({"phone": user_data["phone"]})
        else:
            select_user({"surname": user_data["surname"]})

        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == expected_status
        assert response_data.users is None


# @pytest.mark.skip
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

        current_user = response_data.users[0]

        assert current_user.name == user_data["name"]
        assert current_user.surname == user_data["surname"]
        assert current_user.phone == user_data["phone"]
        assert current_user.age == user_data["age"]


# @pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"name": name_utils.cyrillic_string()}, "success"),
    ({"name": name_utils.latin_string()}, "success"),
    ({"name": name_utils.alphanumeric_string()}, "failure"),
    ({"name": name_utils.special_string()}, "failure"),
    ({"name": name_utils.long_string()}, "failure"),
    ({"surname": name_utils.mixed_alphabet_string()}, "failure"),
    ({"name": name_utils.short_string()}, "failure"),
    ({"name": name_utils.max_string()}, "success"),
    ({"name": name_utils.min_string()}, "success")
], ids=["valid_cyrillic_name", "valid_latin_name", "invalid_alphanumeric_name", "invalid_special_chars_name",
        "invalid_long_name", "invalid_mixed_alphabet_name", "invalid_short_name", "valid_max_length_name",
        "valid_min_length_name"], indirect=True)
def test_add_users_with_different_types_of_names(ws_connection, select_user, add_user, user_data, delete_user,
                                                 parse_response,
                                                 expected_status):
    """
          Добавление юзеров с разными классами эквивалентности в имени
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        if expected_status == "success":
            assert len(response_data.users) == 1

            current_user = response_data.users[0]

            assert current_user.name == user_data["name"]
            assert current_user.surname == user_data["surname"]
            assert current_user.phone == user_data["phone"]
            assert current_user.age == user_data["age"]


# @pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"surname": name_utils.cyrillic_string()}, "success"),
    ({"surname": name_utils.latin_string()}, "success"),
    ({"surname": name_utils.alphanumeric_string()}, "failure"),
    ({"surname": name_utils.special_string()}, "failure"),
    ({"surname": name_utils.long_string()}, "failure"),
    ({"surname": name_utils.mixed_alphabet_string()}, "failure"),
    ({"name": name_utils.short_string()}, "failure"),
    ({"name": name_utils.max_string()}, "success"),
    ({"name": name_utils.min_string()}, "success")
], ids=["valid_cyrillic_surname", "valid_latin_surname", "invalid_alphanumeric_surname",
        "invalid_special_chars_surname",
        "invalid_long_surname", "invalid_mixed_alphabet_surname", "invalid_short_surname", "valid_max_length_surname",
        "valid_min_length_surname"], indirect=True)
def test_add_users_with_different_types_of_surnames(ws_connection, select_user, add_user, user_data, delete_user,
                                                    parse_response,
                                                    expected_status):
    """
          Добавление юзеров с разными классами эквивалентности в фамилии
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        if expected_status == "success":
            assert len(response_data.users) == 1

            current_user = response_data.users[0]

            assert current_user.name == user_data["name"]
            assert current_user.surname == user_data["surname"]
            assert current_user.phone == user_data["phone"]
            assert current_user.age == user_data["age"]


# @pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"age": age_utils.str_age()}, "failure"),
    ({"age": age_utils.int_age()}, "success"),
    ({"age": age_utils.float_age()}, "failure"),
    ({"age": age_utils.negative_age()}, "failure"),
    ({"age": age_utils.maximum_age()}, "success"),
    ({"age": age_utils.minimum_age()}, "success"),
    ({"age": age_utils.underqualified_age()}, "failure"),
    ({"age": age_utils.overqualified_age()}, "failure")
], ids=[
    "invalid_str_age", "valid_int_age", "invalid_float_age", "invalid_negative_age",
    "valid_maximum_age", "valid_minimum_age", "invalid_underqualified_age", "invalid_overqualified_age"], indirect=True)
def test_add_users_with_different_types_of_ages(ws_connection, select_user, add_user, user_data, delete_user,
                                                parse_response,
                                                expected_status):
    """
          Добавление юзеров с разными классами эквивалентности в возрасте
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())

        assert response_data.status == expected_status
        if isinstance(user_data["age"], str):
            assert response_data.reason == ReasonErrorMessages.MUST_BE_NUMBER_NOT_STRING.value
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        if expected_status == "success":
            assert len(response_data.users) == 1

            current_user = response_data.users[0]

            assert current_user.name == user_data["name"]
            assert current_user.surname == user_data["surname"]
            assert current_user.phone == user_data["phone"]
            assert current_user.age == user_data["age"]


# @pytest.mark.skip
@pytest.mark.parametrize("user_data, expected_status", [
    ({"surname": name_utils.cyrillic_string()}, "success"),
    ({"surname": name_utils.latin_string()}, "success"),
    ({"surname": name_utils.alphanumeric_string()}, "failure"),
    ({"surname": name_utils.special_string()}, "failure"),
    ({"surname": name_utils.long_string()}, "failure"),
    ({"surname": name_utils.mixed_alphabet_string()}, "failure"),
    ({"name": name_utils.short_string()}, "failure"),
    ({"name": name_utils.max_string()}, "success"),
    ({"name": name_utils.min_string()}, "success")
], ids=["valid_cyrillic_surname", "valid_latin_surname", "invalid_alphanumeric_surname",
        "invalid_special_chars_surname",
        "invalid_long_surname", "invalid_mixed_alphabet_surname", "invalid_short_surname", "valid_max_length_surname",
        "valid_min_length_surname"], indirect=True)
def test_add_users_with_different_types_of_surnames(ws_connection, select_user, add_user, user_data, delete_user,
                                                    parse_response,
                                                    expected_status):
    """
          Добавление юзеров с разными классами эквивалентности в фамилии
          """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == expected_status
        assert response_data.method == "add"
        assert response_data.id == user_data["id"]

    with allure.step(f"Selecting user with data: {user_data}"):
        select_user({"phone": user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        if expected_status == "success":
            assert len(response_data.users) == 1

            current_user = response_data.users[0]

            assert current_user.name == user_data["name"]
            assert current_user.surname == user_data["surname"]
            assert current_user.phone == user_data["phone"]
            assert current_user.age == user_data["age"]


# @pytest.mark.skip
@pytest.mark.parametrize("get_user_data_list", [{"user1": {"phone": static_phone},
                                                 "user2": {"phone": static_phone}}],
                         ids=["two_users_one_phone"], indirect=True)
def test_add_two_users_with_same_phone(ws_connection, select_user, get_user_data_list, add_user, parse_response):
    """
          Добавление двух юзеров с одинаковым телефоном
          """
    first_user_data = get_user_data_list[0]
    second_user_data = get_user_data_list[1]

    with allure.step(f"Adding first user with data: {first_user_data}"):
        add_user(first_user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == first_user_data["id"]

    with allure.step(f"Selecting user with data: {first_user_data}"):
        select_user({"phone": first_user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == first_user_data["name"]
        assert current_user.surname == first_user_data["surname"]
        assert current_user.phone == first_user_data["phone"]
        assert current_user.age == first_user_data["age"]

    with allure.step(f"Adding second user with data: {second_user_data}"):
        add_user(second_user_data)
        response_data = parse_response(ws_connection.recv())
        assert response_data.status == "failure"
        assert response_data.method == "add"
        assert response_data.id == second_user_data["id"]

    with allure.step(f"Selecting user with data: {first_user_data}"):
        select_user({"phone": first_user_data["phone"]})
        response_data = parse_response(ws_connection.recv())

        assert response_data.method == "select"
        assert response_data.status == "failure"
        assert len(response_data.users) == 1

        current_user = response_data.users[0]

        assert current_user.name == first_user_data["name"]
        assert current_user.surname == first_user_data["surname"]
        assert current_user.phone == first_user_data["phone"]
        assert current_user.age == first_user_data["age"]
