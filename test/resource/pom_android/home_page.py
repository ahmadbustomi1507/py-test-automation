import allure


class HomePage(object):
    def __init__(self,mobile_driver,wait):
        self.mobile_driver = mobile_driver
        self.wait = wait

    def click(self,by,el):
        with allure.step(f"Click {el}"):
            return self.mobile_driver.find_element(
                by=by, value=el
            ).click()

