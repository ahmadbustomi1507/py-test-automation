
# external_markers
from test.utility.api.api_markers import api_test
from test.utility.mobile.mobile_markers import mobile_test
from test.utility.web.web_markers import web_test

def markers():
    external_markers = dict(**api_test,**mobile_test,**web_test)
    return external_markers

