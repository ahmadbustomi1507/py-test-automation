from selenium.webdriver.common.by import By


class HomePage(object):
    sample =(By.CSS_SELECTOR,"selector")

    def __init__(self,driver):
        self.driver = driver

    def shop_items(self):
        self.driver.find_element(HomePage.sample)
