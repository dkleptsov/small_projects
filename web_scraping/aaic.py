from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()

driver.get("https://aaic2021.b2match.io/login")
for i in range (141, 142):
    aaic_url = f"https://aaic2021.b2match.io/participants/{i}"
    driver.get(aaic_url)
    sleep(100)




sleep(5)
driver.quit()