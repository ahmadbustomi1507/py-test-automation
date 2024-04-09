import pytest

@pytest.mark.environment
def test_environment_qa(app_config):
    assert app_config.base_url == "https//myqa-env.com"

@pytest.mark.environment
def test_environment_dev(app_config):
    assert app_config.base_url == "https//mydev-env.com"

@pytest.mark.environment
@pytest.mark.skip(reason="""
we won't test this due to the dev still on progres
""")
def test_environment_qa_2(app_config):
    assert app_config.base_url == "https//myqa-env.com"

@pytest.mark.environment
@pytest.mark.xfail(reason="""
dev still on progress
""")
def test_always_failed(app_config):
    assert False


