import os
import pytest
from selenium.webdriver.common.by import By
from test.utility import api_builder


def check_product_by_api():
    #Check API
    api_test = api_builder.RestApiBuilder("https://public-api.wordpress.com/rest/v1/products?&currency=null&locale=en&product_slugs=dotblog_domain,show-star,dotstore_domain,show-star,dotonline_domain,show-star,dotart_domain,show-star,domain_reg")
    response = api_test.send_get_request()
    response_dict = response.json()
    return response_dict, response_dict.keys(), response.status_code



@pytest.mark.api
@pytest.mark.skip
def test_verify_ui_api_response(log_stream,browser):
    #step 1: check the product and price by API call
    response_dict,response_dict_keys,status_code = check_product_by_api()
    if not (status_code == 200) :
        log_stream.warning(f"api is sick not 200, but {status_code}")

    #step 2: check then product and price by selenium (check to web ui)
    browser.get("https://wordpress.com/domains/?aff=15767&cid=1654213")
    list_product = []
    el_products = browser.find_elements(By.CSS_SELECTOR,'div.lp-image__content span span.lp-lazy-image__content img[src$="svg"]')
    for el_product in el_products:
        path,product_name = os.path.split(el_product.get_attribute("src"))
        list_product.append("dot"+product_name.split(".")[0]+"_domain")

    list_prices =[]
    el_prices = browser.find_elements(By.CSS_SELECTOR,'div p span[class*="lp-product-price__current-price--on-sale"]')
    for el_price in el_prices:
        list_prices.append(el_price.text)

    product_with_price = zip(list_product,list_prices)

    log_stream.info(f'The web display (product,price) = {product_with_price}')


    #Step 3: assertion
    for product,price in product_with_price:
        # price_from_ui = unicodedata.normalize("NFKD",response_dict[product]["combined_sale_cost_display"])
        # assert price_from_ui == price

        match response_dict[product]["currency_code"]:
            case "IDR":
                currency = "Rp"
            case "USD":
                currency = "$"
            case _:
                currency = None

        price_from_ui = f"{currency} {response_dict[product]["sale_cost"]:,.2f}"
        log_stream.info(f"For the product {product} The api return response body as {price_from_ui}")
        log_stream.info(f"Verify value WEB equal to API ")

        if (price != price_from_ui):
            assert False, f"INCORRECT!!! Web Not equal to API web={price} api={price_from_ui}"
        else:
            assert True
            log_stream.info("CORRECT!!! WEB equal to API")
