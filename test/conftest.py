import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.webdriver.appium_service import AppiumService
from pytest import fixture
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import  ChromeDriverManager

# Remote Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


from test import external_markers
from test.utility.config import Config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import pdb
from test.utility.web.web_config_parser import WebConfigParser


# ================================================================
# ENVIRONMENT SETUP => initialization hooks
# ================================================================
def pytest_addoption(parser):
    parser.addoption("--browser",
                     action="store",
                     help="browser to be tested",
                     default=None)
    parser.addoption("--host",
                     action="store",
                     help="host for remote testing",
                     default=None)
    parser.addoption("--port",
                     action="store",
                     help="port for remote testing",
                     default=None)
def pytest_configure(config):
    #add markers manually
    for mark_name in external_markers.markers.keys():
        config.addinivalue_line("markers",f"{mark_name}: {external_markers.markers.get(mark_name)}")

    # Sample to add another option in file <pytest.ini>
    # config.addinivalue_line("key","something")

# ================================================================
# WEB FIXTURE
# ================================================================
@pytest.fixture(scope="module")
def web_configuration(pytestconfig,request):
    print(f"File pytest.ini is in : {pytestconfig.inipath}")
    web_project_config = WebConfigParser(pytestconfig.inipath)
    web_config=dict()
    web_config["username"] = web_project_config.get_config("username").strip()
    web_config["password"] = web_project_config.get_config("password").strip()
    web_config["env"] = web_project_config.get_config("env").strip()
    web_config["url"] = web_project_config.get_config("url").strip()
    return web_config

@pytest.fixture(scope="function")
def web_log(caplog):
    logger = logging.getLogger(__name__)
    caplog.clear()
    return logger

@fixture(scope="function")
def browser(request,web_configuration,web_log):
    #########################################################
    # SETUP THE WEB TEST
    #########################################################
    browser_name = request.config.getoption("--browser")
    # TO DO : how we handle if browser_name is empty??
    if browser_name is None:
        browser_name = "chrome"

    hub_host = request.config.getoption("--host")
    # TO DO : how we handle if hub_host is empty??
    if hub_host is None:
        hub_host = "http://localhost"

    hub_port = request.config.getoption("--port")
    # TO DO : how we handle if browser_name is empty??
    if hub_port is None:
        hub_port = "4444"


    match str(browser_name):
        case "chrome":
            driver = webdriver.Remote(options=ChromeOptions(),command_executor=f"{hub_host}:{hub_port}")
            wait = WebDriverWait(driver=driver,timeout=5)
        case "firefox":
            driver = webdriver.Remote(options=FirefoxOptions(),command_executor=f"{hub_host}:{hub_port}")
            wait = WebDriverWait(driver=driver,timeout=5)
        case "edge":
            driver = webdriver.Remote(options=EdgeOptions(),command_executor=f"{hub_host}:{hub_port}")
            wait = WebDriverWait(driver=driver,timeout=5)
        case _:
            driver = None
            wait = None
            #request.raiseerror("cannot find the driver")

    web_log.info(f"Starting Web AutomationTest with browser: {browser_name}")
    web_log.info(f"Base Url: {web_configuration["url"]}" )
    web_log.info(f"Env: {web_configuration["env"]}")
    web_log.info(f"Running Selenium Remote Driver : <{hub_host}:{hub_port}>" )
    logging.info(f"this is using loggin")
    web_log.info(f"this is using web_log")

    yield driver,wait
    #########################################################
    # TEARDOWN THE WEB TEST
    #########################################################
    driver.quit()


# ================================================================
# MOBILE FIXTURE
# ================================================================

@pytest.fixture(scope="module")
def mobile_configuration(pytestconfig,request):
    print(f"File pytest.ini is in : {pytestconfig.inipath}")
    web_project_config = WebConfigParser(pytestconfig.inipath)
    web_config=dict()
    web_config["username"] = web_project_config.get_config("username").strip()
    web_config["password"] = web_project_config.get_config("password").strip()
    web_config["env"] = web_project_config.get_config("env").strip()
    web_config["url"] = web_project_config.get_config("url").strip()
    return web_config

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


# this appium_service will be used in the test-container
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
