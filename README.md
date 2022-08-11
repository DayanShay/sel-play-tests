# sel-play-tests
sela -  pytest project using selenium and playwright
 
Only browser.Chromiume

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
![image](https://user-images.githubusercontent.com/108628136/184260728-acc17f23-b966-4d16-b127-54ec17300ceb.png)
