
import pytest
from pydantic import ValidationError

from test.utility import api_builder
from test.utility import url
from test.resource.dto.dto_User import  *

@pytest.mark.api
def test_api_A_sample_1(log_stream):
    api_test = api_builder.RestApiBuilder(url.base_url["mockapi"])

    api_test.set_endpoint("/api/v1/users/1")

    r = api_test.send_get_request()

    log_stream.info(f"response {r.json()}")
    try:
        User.model_validate(r.json())
        assert True
    except ValidationError as e:
        log_stream.info(f"Error {e}")
        assert False
