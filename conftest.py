import pytest
import websocket
import json
from configuration import SERVICE_URL
from models.user_data import UserDataGenerator
from models.responce_data import ResponseData



def pytest_configure(config):
    config.addinivalue_line(
        "markers", "old: marks old tests"
    )
    config.addinivalue_line(
        "markers", "new: marks new tests"
    )
    config.addinivalue_line(
        "markers", "hmm: marks hmm tests"
    )
    config.addinivalue_line(
        "markers", "delete: marks hmm tests"
    )


@pytest.fixture
def ws_connection(autouse=True):
    ws = websocket.create_connection(SERVICE_URL)
    ws.settimeout(2)
    yield ws
    ws.close()


@pytest.fixture
def expected_status(request):
    return request.param

@pytest.fixture
def expected_reason(request):
    if hasattr(request, 'param'):
        return request.param

@pytest.fixture
def parse_response():
    def _parse_response(response: str):
        return ResponseData.parse_raw(response)

    return _parse_response


@pytest.fixture
def get_user_data_list(request):
    user_data_list = []
    for user in request.param:
        user_data_list.append(UserDataGenerator(**request.param[user]).data)
    return user_data_list


@pytest.fixture
def user_data(request):
    if hasattr(request, 'param'):
        return UserDataGenerator(**request.param).data
    else:
        return UserDataGenerator().data

@pytest.fixture
def extra_field(request):
    return request.param


@pytest.fixture
def check_response(expected_status, method):
    def _check_response(response: str):
        resp_data = ResponseData.parse_raw(response)
        assert resp_data.status == expected_status
        assert resp_data.method == method
        assert resp_data.id == "sfda-11231-123-adfa"
        return resp_data

    return _check_response


@pytest.fixture
def add_user(ws_connection, delete_user, user_data):
    def _add_user(user_data):
        # отправка запроса с данными пользователя
        request = {
            "method": "add",
            **user_data
        }
        ws_connection.send(json.dumps(request))

    yield _add_user

    # teardown
    if "phone" in user_data:
        delete_user({"phone": user_data["phone"]})





@pytest.fixture
def delete_user(ws_connection):
    def _delete_user(user_data):
        # отправка запроса с данными пользователя
        request = {
            "method": "delete",
            **user_data
        }
        ws_connection.send(json.dumps(request))

    return _delete_user


@pytest.fixture
def select_user(ws_connection):
    def _select_user(user_data):
        # отправка запроса с данными пользователя
        request = {
            "id": "123412-adf-13213",
            "method": "select",
            **user_data
        }
        ws_connection.send(json.dumps(request))

        # проверка статуса
        # response = ws_connection.recv()
        # assert json.loads(response)["status"] == expected_status
        # assert json.loads(response)["method"] == "select"
        # assert json.loads(response)["id"] == "123412-adf-13213"

    return _select_user

@pytest.fixture
def update_user(ws_connection):
    def _update_user(user_data):
        # отправка запроса с данными пользователя
        request = {
            "id": "123412-adf-13213",
            "method": "update",
            **user_data
        }
        ws_connection.send(json.dumps(request))

        # проверка статуса
        # response = ws_connection.recv()
        # assert json.loads(response)["status"] == expected_status
        # assert json.loads(response)["method"] == "select"
        # assert json.loads(response)["id"] == "123412-adf-13213"

    return _update_user
