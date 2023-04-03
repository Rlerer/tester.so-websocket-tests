import pytest
import allure
def test_select_user_12(ws_connection, add_user, user_data, delete_user, expected_status, parse_response):
    """
        удаляем челов с кастомным статусом
        """
    with allure.step(f"Adding user with data: {user_data}"):
        add_user(user_data, expected_status)
        response = ws_connection.recv()
        response_data = parse_response(response)
        request_data = user_data
        assert response_data.status == "success"
        assert response_data.method == "add"
        assert response_data.id == request_data["id"]
