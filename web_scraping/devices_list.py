import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ENTRY_URL = "TTT"
LOGIN = "YYY"
PASS = "UUU"
LOGIN_PATH = "/html/body/div[1]/section/div[2]/div[2]/div[2]/div[1]/input"
PASS_PATH = "/html/body/div[1]/section/div[2]/div[2]/div[2]/div[2]/input"
MORE_ID = "moreDevice"
MORE_PATH = "/html/body/div/section/article/div/div/div[3]/div[1]/div[4]/span"
TABLE_PATH = "/html/body/div/section/article/div/div/div[3]/div[1]"
SLEEP_TIME = 2


def get_info():
    driver = webdriver.Firefox()
    driver.get(ENTRY_URL)
    # Логинимся
    driver.find_element_by_xpath(LOGIN_PATH).send_keys(LOGIN)
    driver.find_element_by_xpath(PASS_PATH).send_keys(PASS)
    driver.find_element_by_xpath(PASS_PATH).send_keys(Keys.ENTER)
    sleep(SLEEP_TIME)

    # Получаем список всех устройств
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 
                  MORE_ID))).click()
    info = driver.find_element_by_xpath(TABLE_PATH).text
    driver.quit()
    
    return info


def main():
    print(get_info())


if __name__ == "__main__":
    main()
