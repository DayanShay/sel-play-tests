import time
import logging
import pytest
from playwright.sync_api import sync_playwright
from data import *

Test_log = logging.getLogger()


@pytest.fixture
def open_page():
    """
    function will open the page of
    :return: None
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://automationpractice.com/index.php")
        yield page
        page.close()


def test_login_with_correct_details(open_page:sync_playwright)->None:
    """
    test login with right details to website
    :param open_page: sync_playwright: website driver page
    :return: None
    """
    page = open_page
    page.wait_for_timeout(3)
    page.click('.login')
    page.locator('id=email').fill(right_user[0])
    page.locator('id=passwd').fill(right_user[1])
    page.locator('id=SubmitLogin').click()
    Test_log.info(f"You have logged on to {page.title()}")
    assert page.title() == 'My account - My Store'


def test_login_with_wrong_details(open_page:sync_playwright)->None:
    """
    test login with test_login_wrong details to website from userslist
    :param open_page:  sync_playwright: website driver page
    :return: None
    """
    page = open_page
    page.wait_for_timeout(3)
    page.click('.login')
    for user in wrong_users_list:
        page.locator('id=email').fill(user[0])
        page.locator('id=passwd').fill(user[1])
        page.locator('id=SubmitLogin').click()
        time.sleep(1)
        msg_error = page.locator('id=center_column')
        error = msg_error.locator('.alert').all_text_contents()
        Test_log.info(f"Loging details = {user} , {error[0].strip()}")
        assert page.title() == 'Login - My Store'


def test_forget_password_button(open_page:sync_playwright)->None:
    """
    function clicking on forget password in login form.
    :param open_page: sync_playwright: website driver page
    :return: None
    """
    page = open_page
    page.click('.login')
    page.wait_for_timeout(3)
    page.locator('text="Forgot your password?"').click()
    Test_log.info(f"You are on page {page.title()}")
    assert page.title() == 'Forgot your password - My Store'


def test_find_and_buy_cheap(open_page:sync_playwright)->None:
    """
    function log in the website and  find the cheapest product under summer search and complete Buying
    :param test_open: sync_playwright: website driver page
    :return: None
    """

    # log in with correct user and password

    test_login_with_correct_details(open_page)

    # after log in going to search summer

    open_page.locator('id=search_query_top').fill('summer')
    open_page.locator('xpath=//*[@id="searchbox"]/button').click()

    # Takes time for the website to load all products
    time.sleep(3)

    # finding relevant products - and make a Dict[price:product]

    product_list = open_page.query_selector_all(".product-container")
    price_list = {}
    for product in product_list:
        price = product.query_selector(".product-price").text_content().strip()
        # Dict[price:product]
        price_list[price] = product

    # finding cheap dress - and make a click on it
    cheapes = min(price_list.keys())
    price_list[cheapes].click()

    # clicking add to cart
    price_list[cheapes].query_selector('.ajax_add_to_cart_button').click()
    open_page.wait_for_timeout(3)
    open_page.locator("text=Proceed to checkout").click()

    # Starting buying process

    for i in range(5):
        Test_log.info(f"{open_page.title()}")
        time.sleep(2)
        if i == 2:
            open_page.locator('id=cgv').click()
        if i == 3:
            open_page.locator('text=Pay by bank wire').last.click()
            continue
        if i == 4:
            open_page.locator('.cart_navigation').click()
            open_page.locator('xpath=//*[@id="cart_navigation"]/button').click()
            continue
        open_page.locator('text=Proceed to checkout').last.click()

    # Finish buying process

    Test_log.info(f"{open_page.title()}")
    assert "Order confirmation - My Store" == open_page.title()
