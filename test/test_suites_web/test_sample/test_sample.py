
from pytest import mark
@mark.sample
def test_aduhai(browser,web_log):
    web_log.info("im using log from fixture")
