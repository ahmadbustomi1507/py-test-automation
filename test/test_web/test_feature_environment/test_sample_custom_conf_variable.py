import pytest
from test.utility.project_config_parser import ProjectConfigParser

@pytest.mark.parametrize_sample
def test_sample_custom_conf_variable_1():
    my_config_sample = ProjectConfigParser()
    for index,my_config in enumerate(my_config_sample.get_list_project_config()):
        print(f"\nthis is project config {index} {my_config} : {my_config_sample.get_config(my_config)}")
    assert True