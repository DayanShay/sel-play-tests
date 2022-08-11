# sel-play-tests
sela -  pytest project using selenium and playwright
 
MAST DO BEFORE
relocate chromedriver.exe in project folder 

How to Run on cmd - make sure to copy the full path to the tests file.

pytest "FullPath"\playwright\test_playwright.py


For allure report
Need to have

allure install
And JAVA_HOME
To run Allure Report

1. *pytest --alluredir=playwrightReports\ ."FullPath"\playwright\test_playwright.py*

2. *allure serve .\"FullPath"\playwright\playwrightReports*

exemple :
