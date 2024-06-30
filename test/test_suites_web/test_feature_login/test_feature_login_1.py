import pytest

# from test.resource.pom_web.home_page import HomePage
# from test.resource.pom_web.login_page import LoginPage

@pytest.mark.web_selenium
class TestFeatureLogin(object):
    def test_A_feature_login_1(self,browser,log_stream):
        driver,wait = browser
        # home_page = HomePage(driver)
        # login_page = LoginPage(driver)

        #explicit wait
        wait.until_ID("someID")
        
        # print(f"this is home_page {home_page.sample}")
        # print(f"this is login_page {login_page.sample}")
        assert True
