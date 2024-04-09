import os
import pytest
from test.utility import extraction

@pytest.mark.api
@pytest.mark.skip
def test_api_sample_ddt_1():
    print(f"\nthis is my file 1 {os.path.dirname(os.path.abspath(__file__))}")
    print(f"\nthis is my file 2 {os.getcwd()}")
    print(f"\nthis is my file 3 {os.path.abspath(__file__)}")
    currdir = os.getcwd()

    print(f"\nthis is my file 4 {os.path.join(currdir,"test","resource","data")}")

@pytest.mark.parametrize("test_data",extraction.extract_my_json(extraction.DATA_PATH))
@pytest.mark.api
@pytest.mark.skip
def test_api_sample_ddt_2(test_data):
    print(f"\nthis is my current resource {test_data}")
