import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import  ChromeDriverManager
from test.utility.config import Config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging


# ================================================================
# ENVIRONMENT SETUP
# ================================================================


# ================================================================
# WEB FIXTURE
# ================================================================
@fixture(scope='function',params=[
    "chrome"
])
def browser():
    driver = get_browser_driver(request.param)
    wait = WebDriverWait(driver=driver,timeout=5)

    def wait_until_ID(by, el):
        try:
            wait.until(EC.presence_of_element_located(
                (By.ID, el)
            ))
        except:
            raise Exception(f"Couldnt find the element {el}")
            return f"Couldnt find the element {el}"

        return f"{el} has been found"


    yield driver,wait



    #teardown
    driver.quit()

def get_browser_driver(browser_name):
    driver = None
    match str(browser_name):
        case "chrome":
            # os.environ['WDM_LOCAL'] ='1'
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        case "firefox":
            pass
        case _:
            raise Exception("Unknown browser")
    return driver



#initialization hook
@fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@fixture(scope='session')
def app_config(env):
    return Config(env)

# adding option in command line
def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     help="environment to run tests")

@pytest.fixture(scope="function")
def log_stream(caplog):
    logger = logging.getLogger(__name__)
    caplog.clear()
    return logger
# ================================================================
# MOBILE FIXTURE
# ================================================================

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'

def create_android_driver():
    capabilities = {
        "platformName": "android",
        "appium:platformVersion": "10.0",
        "appium:app": "C:\\Kerja\\git\\py-test-automation\\test\\resource\\apk\\ApiDemos-debug.apk",
        "appium:deviceName": "emulator-5554",
        "appium:noReset": False
    }
    return webdriver.Remote(f"http://{APPIUM_HOST}:{APPIUM_PORT}/wd/hub",
                            options=UiAutomator2Options().load_capabilities(capabilities))


def create_ios_driver():
    options = XCUITestOptions()
    options.platformVersion = '13.4'
    options.udid = '123456789ABC'

    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}/wd/hub', options=options)


@pytest.fixture(scope="function")
def mobile_driver():
    driver = create_android_driver()

    def wait_until(by, el):
        try:
            driver.implicitly_wait(2)
            driver.find_element(AppiumBy=by, value=el)

        except:
            raise Exception(f"Couldnt find the element {el}")
            return f"Couldnt find the element {el}"
        return f"{el} has been found"

    yield driver, wait_until
    driver.quit()


# this appium_service will be used in the container
# if you are running in local, dont use this fixture or simply comment
@pytest.fixture(scope='session')
def appium_service():
    service = AppiumService()
    service.start(
        args=['--address', APPIUM_HOST,
              '-p', str(APPIUM_PORT),
              '--base-path', "/wd/hub",
              '--log-level', "info:info"],
        timeout_ms=60000
    )
    yield service
    service.stop()
