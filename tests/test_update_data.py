import allure
import pytest
from helpers import Helpers
from api_methods.update_data import UpdateUserData

helper = Helpers()


class TestUpdateUser:
    @allure.title("Authorized user update")
    @allure.description("Existing user update with new credentials")
    @pytest.mark.parametrize('payload',
                             [{"email": f'{helper.generate_credentials()["email"]}'},
                              {"name": f'{helper.generate_credentials()["name"]}'}])
    def test_update_successful(self, user_create_and_delete, payload):
        token = user_create_and_delete[2]
        update = UpdateUserData()
        response_patch = update.update_data(payload, token)
        payload_key = list(payload.keys())[0]
        assert response_patch.status_code == 200 and payload[payload_key] == response_patch.json()["user"][payload_key]

    @allure.title("Unauthorized user update")
    @allure.description("Unauthorized user update with new credentials")
    def test_update_error(self, user_create_and_delete):
        token = None
        update = UpdateUserData()
        response_patch = update.update_data(user_create_and_delete[1], token)
        assert response_patch.status_code == 401 and response_patch.json()["message"] == "You should be authorised"

