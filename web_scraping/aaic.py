from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

MESSAGE = 'Hello! How are you doing?\
\nCurrently I am studying Deep learning and I really want to apply my knowledge to real life projects. \
\nPlease let me know If you have any projects where we might use Artificial Intelligence (AI).\
\nI have experience in Natural language processing and Computer vision.\
\nYou can find full list of my certificates on my LinkeIn page: https://www.linkedin.com/in/kleptsov/ \
\nI can work as an employee or as a contractor.\
\nIf you wish, we can arrange a video conference (e.g. "Zoom") outside of this conference to discuss all details and possibilities.\
\nAlso I can create web and telegram bots to automate different tasks.\
\nThanks in advance. I look forward to hearing from you. Kind regards.\
\nDenis Kleptsov'

driver = webdriver.Chrome()
driver.get("https://aaic2021.b2match.io/login")

# Логинимся
driver.find_element_by_id('Email').send_keys('denis@kleptsov.com')
driver.find_element_by_id('Password').send_keys('busumsp1')
driver.find_element_by_id('Password').send_keys(Keys.ENTER)

for i in range (200, 1500):
    aaic_url = f"https://aaic2021.b2match.io/participants/{i}"
    driver.get(aaic_url)
    sleep(1)
    try:
        driver.find_element_by_xpath("/html/body/section/main/section/div/div[1]/div/div[3]/a").click()
        sleep(1)
        driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div/div[2]/form/div/div/textarea").send_keys(MESSAGE)
        driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div/div[2]/form/div/div/div/button[2]").click()
        sleep(2)
    except:
        sleep(1)


    sleep(2)




sleep(500)
driver.quit()