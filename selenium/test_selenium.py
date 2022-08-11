import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from data import *

Test_log = logging.getLogger()


@pytest.fixture
def test_open():
    driver = webdriver.Chrome(path_driver)
    driver.maximize_window()
    yield driver
    driver.quit()

def log_in_auto(driver:webdriver.Chrome,email :str,password:str):
    page = driver
    page.get('http://automationpractice.com/index.php')
    driver.find_element(By.CLASS_NAME, "login").click()
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "passwd").send_keys(password)
    driver.find_element(By.NAME, "SubmitLogin").click()

def test_login_right(test_open:webdriver.Chrome):
    log_in_auto(driver=test_open, email=right_user[0], password=right_user[1])
    res = test_open.find_element(By.CLASS_NAME, "account")
    username = res.find_element(By.TAG_NAME, "span").text
    # loging info
    assert username == 'shay dayan'

def test_login_wrong(test_open):
    for users in wrong_users_list:
        log_in_auto(test_open,email=users[0],password=users[1])
        msg_error = test_open.find_element(By.CLASS_NAME, "alert")
        error = msg_error.find_element(By.TAG_NAME,"p")
        # loging info
        print(msg_error.find_element(By.TAG_NAME,"ol").text)
        assert "error" in error.text

def test_buy_a_dress(test_open):
    driver = test_open
    driver.implicitly_wait(3)

    # log in with correct user and password
    log_in_auto(driver=driver,password=right_user[1],email=right_user[0])
    res = test_open.find_element(By.CLASS_NAME, "account")
    username = res.find_element(By.TAG_NAME, "span").text
    # loging info
    assert username == 'shay dayan'

    # after log in going to search summer
    driver.find_element(By.NAME, "search_query").send_keys("summer")
    driver.find_element(By.NAME, "submit_search").click()
    driver.implicitly_wait(3)

    # finding relevant products - and make a Dict[price:product]
    product_list = driver.find_element(By.CLASS_NAME,"product_list")
    product_containers = product_list.find_elements(By.CLASS_NAME,"product-container")
    price_list = {}
    for product_container in product_containers:
        right_block = product_container.find_element(By.CLASS_NAME,"right-block")
        content_price = right_block.find_element(By.CLASS_NAME,"content_price")
        price = content_price.find_element(By.TAG_NAME,"span").text
        # Dict[price:product]
        price_list[price.strip()] = right_block

    # finding cheap dress - and make a click on it
    cheapest = min(price_list.keys())

    # Starting buying process

    price_list[cheapest].click()
    button_section =price_list[cheapest].find_element(By.CLASS_NAME, "button-container")

    # clicking add to cart
    button_section.find_element(By.TAG_NAME, "span").click()

    # clicking on pop up
    add_to_cart = driver.find_element(By.CLASS_NAME, "button-container")
    driver.implicitly_wait(5)
    add_to_cart.find_element(By.TAG_NAME,"a").click()

    # Starting order process
    for i in range(5):
        Test_log.info(f"{driver.title}   step{i+1}")
        if i ==1:
            driver.implicitly_wait(3)
            driver.find_element(By.NAME,"processAddress").click()
            continue
        if i ==2:
            driver.implicitly_wait(3)
            driver.find_element(By.ID,"uniform-cgv").click()
            driver.find_element(By.NAME,"processCarrier").click()
            continue
        if i ==3:
            driver.implicitly_wait(3)
            driver.find_element(By.CLASS_NAME,"bankwire").click()
            continue
        if i ==4:
            driver.implicitly_wait(3)
            right_pass = driver.find_element(By.ID,"cart_navigation")
            right_pass.find_element(By.TAG_NAME,"button").click()
            text = driver.find_element(By.CLASS_NAME,"box").text
            continue
        driver.implicitly_wait(3)
        driver.find_element(By.LINK_TEXT, "Proceed to checkout").click()
    # loging info
    Test_log.info(f'{text[0:36]}')
    assert "Your order on My Store is complete." in text

def test_forgat_passwd(test_open)->None:
    driver = test_open
    driver.get('http://automationpractice.com/index.php')
    driver.find_element(By.CLASS_NAME, "login").click()
    driver.find_element(By.LINK_TEXT, "Forgot your password?").click()
    Test_log.info(f"{driver.title}")
    assert driver.title == 'Forgot your password - My Store'

