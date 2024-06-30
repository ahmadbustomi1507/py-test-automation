
# Test Runner
import pytest
# Selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# Appium

# Automation driver for mobile
from appium.options.android import UiAutomator2Options

# Remote Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from test.utility.api.api_config_parser import ApiConfigParser
# Configuration file
from test.utility.mobile.mobile_config_parser import MobileConfigParser
from test.utility.web.web_config_parser import WebConfigParser

# Miscellaneous
import logging
from os import path
from test.utility.external_markers import markers


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

    parser.addoption("--platformName",
                     action="store",
                     help="platform name either android/ios, for example 'android'",
                     default="android")
    parser.addoption("--platformVersion",
                     action="store",
                     help="platform name either android/ios, for example '10'",
                     default="10")
    parser.addoption("--deviceName",
                     action="store",
                     help="deviceName either android/ios",
                     default="android")

def pytest_configure(config):
    #add markers manually
    for mark_name in markers().keys():
        config.addinivalue_line("markers",f"{mark_name}: {markers().get(mark_name)}")

    # Sample to add another option in file <pytest.ini>
    # config.addinivalue_line("key","something")

@pytest.fixture(scope="function")
def log(caplog):
    logger = logging.getLogger(__name__)
    caplog.clear()
    return logger

# ================================================================
# WEB FIXTURE
# ================================================================
@pytest.fixture(scope="module")
def web_configuration(pytestconfig,request):
    # print(f"File pytest.ini is in : {pytestconfig.inipath}")
    # print(f"all markers available {pytestconfig.getini('markers')}")

    web_project_config = WebConfigParser(pytestconfig.inipath)
    web_config=dict()
    web_config["username"] = web_project_config.get_config("username").strip()
    web_config["password"] = web_project_config.get_config("password").strip()
    web_config["env"] = web_project_config.get_config("env").strip()
    web_config["url"] = web_project_config.get_config("url").strip()
    return web_config


@pytest.fixture(scope="function")
def browser(request,web_configuration,log):
    #########################################################
    # SETUP THE WEB TEST
    #########################################################
    browser_name = request.config.getoption("--browser")
    # TO DO : how we handle if browser_name is empty??
    # if browser_name is None:
    #     browser_name = "chrome"

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
            request.raiseerror("cannot find the driver")

    log.info(f"Starting Web AutomationTest with browser: {browser_name}")
    log.info(f"Base Url: {web_configuration["url"]}" )
    log.info(f"Env: {web_configuration["env"]}")
    log.info(f"Running Selenium Remote Driver : <{hub_host}:{hub_port}>" )

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
    mobile_project_config = MobileConfigParser(pytestconfig.inipath)
    mobile_config=dict()
    mobile_config["app_path"] = mobile_project_config.get_config("app_path").strip()
    mobile_config["caps_folder"] = mobile_project_config.get_config("caps_folder").strip()
    mobile_config["appium_host"] = mobile_project_config.get_config("appium_host").strip()
    mobile_config["appium_port"] = mobile_project_config.get_config("appium_port").strip()
    mobile_config["android_app_name"] = mobile_project_config.get_config("android_app_name").strip()
    mobile_config["ios_app_name"] = mobile_project_config.get_config("ios_app_name").strip()
    return mobile_config

@pytest.fixture(scope="function")
def mobile(request,mobile_configuration,log):
    #########################################################
    # SETUP THE MOBILE TEST
    #########################################################
    platform_name = request.config.getoption("--platformName")
    platform_version = request.config.getoption("--platformVersion")
    device_name = request.config.getoption("--deviceName")
    no_reset = False

    if (platform_name == "android"):
        app_path = path.join(mobile_configuration['app_path'], "android", mobile_configuration["android_app_name"])
    elif (platform_name == "ios"):
        app_path = path.join(mobile_configuration['app_path'], "ios", mobile_configuration["ios_app_name"])
    else:
        app_path = None

    #BUILD CAPABILITIES
    mobile_caps = dict()
    mobile_caps["platformName"] = platform_name
    mobile_caps["appium:platformVersion"] = platform_version
    mobile_caps["appium:app"] = app_path
    mobile_caps["appium:deviceName"] = device_name
    mobile_caps["appium:noReset"] = no_reset

    if (platform_name == "android"):
        drive = webdriver.Remote(f"http://{mobile_configuration["appium_host"]}:{mobile_configuration["appium_port"]}/wd/hub",
                                options=UiAutomator2Options().load_capabilities(mobile_caps))
    elif (platform_name == "ios"):
        #TO DO : refactor this ios automation
        pass
    else:
        driver = None

    log.info(f"Starting Mobile AutomationTest with device: {device_name} {platform_name}:{platform_version}")
    log.info(f"Appium information : <{mobile_configuration["appium_host"]}:{mobile_configuration["appium_port"]}>")
    if (platform_name == "android"):
        log.info(f"App name : {mobile_configuration["android_app_name"]}")
    elif (platform_name == "ios"):
        log.info(f"App name : {mobile_configuration["ios_app_name"]}")
    yield driver
    #########################################################
    # TEARDOWN THE WEB TEST
    #########################################################
    driver.quit()


# def create_ios_driver():
#     options = XCUITestOptions()
#     options.platformVersion = '13.4'
#     options.udid = '123456789ABC'
#
#     return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}/wd/hub', options=options)


# this appium_service will be used in the test-container
# if you are running in local, dont use this fixture or simply comment
# On progress
# @pytest.fixture(scope='session')
# def appium_service():
#     service = AppiumService()
#     service.start(
#         args=['--address', APPIUM_HOST,
#               '-p', str(APPIUM_PORT),
#               '--base-path', "/wd/hub",
#               '--log-level', "info:info"],
#         timeout_ms=60000
#     )
#     yield service
#     service.stop()

# ================================================================
# API FIXTURE
# ================================================================
#ON Progress
@pytest.fixture(scope="function")
def api(pytestconfig, request, log):
    print(f"File pytest.ini is in : {pytestconfig.inipath}")
    api_project_config = ApiConfigParser(pytestconfig.inipath)
    api_config = dict()
    api_config["env"] = api_project_config.get_config("env").strip()
    api_config["host"] = api_project_config.get_config("env").strip()
    api_config["port"] = api_project_config.get_config("env").strip()
    return api_config
