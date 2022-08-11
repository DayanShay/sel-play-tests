sel-play-tests
sela - pytest project using selenium and playwright

MAST DO BEFORE relocate chromedriver.exe in project folder

How to Run on cmd - make sure to copy the full path to the tests file.

pytest "FullPath"\selenium\test_selenium.py

For allure report Need to have

allure install And JAVA_HOME To run Allure Report

pytest --alluredir=seleniumReports\ ."FullPath"\selenium\test_selenium.py

allure serve ."FullPath"\selenium\seleniumReports

exemple :
![image](https://user-images.githubusercontent.com/108628136/184260834-d16f86a4-e3bd-4716-84e2-a3fa73027830.png)
