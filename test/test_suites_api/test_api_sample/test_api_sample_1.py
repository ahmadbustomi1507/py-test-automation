from pytest import mark
from test.utility.api.api_builder import RestApiBuilder
from test.utility.api.api_config_parser import extract_my_data

@mark.sample_api
@mark.parametrize("context",extract_my_data("./test/test_suites_api/data", "json",with_index=False))
def test_sample_api(context,api):
    # description = context["description"]
    # request = context["request"]
    # print(f"request {request}")
    # response = context["response"]
    build_api = RestApiBuilder(api["host"],api["port"],context)
    build_api.send()
    print(build_api.get_data())

