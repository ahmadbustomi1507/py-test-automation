import allure
import pytest
from test.resource.pom_android.home_page import HomePage
from appium.webdriver.common.appiumby import AppiumBy

@pytest.mark.mobile
@pytest.mark.usefixtures("appium_service")
class Test_android_demo(object):

    @pytest.fixture(scope="function",autouse=True)
    def __get_driver(self,mobile_driver):
        self.driver , self.wait_until = mobile_driver
        self.home = HomePage(self.driver,self.wait_until)

    def test_a_android_demo(self):
        #"Animation"
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID,el="Animation")
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID, el="Cloning")
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID, el="Run")

    def test_b_android_demo(self,mobile):
        #"Animation"
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID,el="Animation")
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID, el="Cloning")
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID, el="Run")

    def test_c_android_demo(self,mobile):
        #"Animation"
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID,el="Animation")
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID, el="Cloning")
        self.home.click(by=AppiumBy.ACCESSIBILITY_ID, el="Run")