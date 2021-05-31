import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# MESSAGE = "Hello! Your profile seems very interesting to me.\
# \nLet's stay in touch on LinkedIn: https://www.linkedin.com/in/kleptsov/\
# \nAlso we can schedule brief online meeting: https://calendly.com/kleptsov\
# \nJust choose time slot that works for you and enter your email. System will take care of the rest.\
# \nKind regards\
# \nDenis"
SLEEP_TIME = 2


# def send_message() -> None:
#     driver = webdriver.Chrome()
#     driver.get("https://aaic2021.b2match.io/login")
#     # Логинимся
#     driver.find_element_by_id('Email').send_keys('denis@kleptsov.com')
#     driver.find_element_by_id('Password').send_keys(os.environ['SIMPLE_PASS'])
#     driver.find_element_by_id('Password').send_keys(Keys.ENTER)
#     sleep(SLEEP_TIME*2)
#     # Рассылаем сообщения
#     errors = 0
#     for i in range (1, 2000):
#         aaic_url = f"https://aaic2021.b2match.io/participants/{i}"
#         driver.get(aaic_url)
#         sleep(SLEEP_TIME)
#         try:
#             if errors < 100:
#                 driver.find_element_by_xpath("/html/body/section/main/section/div/div[1]/div/div[3]/a").click()
#                 sleep(SLEEP_TIME)
#                 driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div/div[2]/form/div/div/textarea").send_keys(MESSAGE)
#                 driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div/div[2]/form/div/div/div/button[2]").click()
#                 print(f"SUCCESS!!!!! Counter: {i}, errors: {errors}")    
#                 sleep(SLEEP_TIME)
#         except:
#             errors += 1
#             print(f"Failed. Counter: {i}, errors: {errors}")
#             sleep(SLEEP_TIME)
#     driver.quit()


# def send_messages_by_list() -> None:
#     driver = webdriver.Firefox()
#     driver.get("https://aaic2021.b2match.io/login")
#     driver.find_element_by_id('Email').send_keys('denis@kleptsov.com')
#     driver.find_element_by_id('Password').send_keys(os.environ['SIMPLE_PASS'])
#     driver.find_element_by_id('Password').send_keys(Keys.ENTER)
#     sleep(SLEEP_TIME*2)

#     # Открываем странички по списку
#     with open("not_replied.txt", "r", encoding="utf-8") as file:
#         url_list = file.readlines()
    
#     errors = 0
#     for url in url_list:
#         driver.get(url)
#         sleep(SLEEP_TIME)
#         try:
#             driver.find_element_by_xpath("/html/body/section/main/section/div/div[1]/div/div[3]/a").click()
#             sleep(SLEEP_TIME*2)
#             driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div/div[2]/form/div/div/textarea").send_keys(MESSAGE)
#             driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div/div[2]/form/div/div/div/button[2]").click()
#             print(f"SUCCESS!!!!! url: {url}, errors: {errors}")    
#             sleep(SLEEP_TIME*2)
#         except:
#             errors += 1
#             print(f"Failed. url: {url}, errors: {errors}")
#             with open('send_errors_1.txt', 'a', encoding="utf-8") as writer:
#                 writer.write(f"\n{url}")
#             sleep(SLEEP_TIME)

#     driver.quit()


def check_replies() -> None:
    driver = webdriver.Firefox()
    driver.get("https://aaic2021.b2match.io/login")
    # Логинимся
    driver.find_element_by_id('Email').send_keys('denis@kleptsov.com')
    driver.find_element_by_id('Password').send_keys(os.environ['SIMPLE_PASS'])
    driver.find_element_by_id('Password').send_keys(Keys.ENTER)
    sleep(SLEEP_TIME*2)
    # Собираем инфу
    errors = 0
    for i in range (2, 2000):
        aaic_url = f"https://aaic2021.b2match.io/participants/{i}"
        driver.get(aaic_url)
        sleep(SLEEP_TIME*2)
        try:
            if errors < 300:
                driver.find_element_by_xpath("/html/body/section/main/section/div/div[1]/div/div[3]/a").click()
                sleep(SLEEP_TIME*3)

                reply = driver.find_elements_by_xpath("/html/body/section/main/div[2]/div/div[2]/div[2]/div/div[2]/div/p[1]")
                if len(reply) > 0:
                    print(f"REPLIED: {aaic_url}")
                    with open('replied.txt', 'a', encoding="utf-8") as writer:
                        writer.write(f"\n{aaic_url}")
                else:
                    print(f"Didn't: {aaic_url}")
                    with open('not_replied.txt', 'a', encoding="utf-8") as writer:
                        writer.write(f"\n{aaic_url}")


                # try:
                #     # ОТВЕТНОЕ СООБЩЕНИЕ
                #     reply = driver.find_element_by_xpath("/html/body/section/main/div[2]/div/div[2]/div[2]/div/div[2]/div/p[1]")
                #     print(reply)
                #     print(reply.text)
                #     # reply_text = reply.text
                #     print(f"REPLIED: {aaic_url}")
                #     sleep(SLEEP_TIME*2)
                # except:
                #     print(f"Didn't: {aaic_url}")
                #     sleep(SLEEP_TIME*2)
                # sleep(SLEEP_TIME*2)
        except:
            errors += 1
            print(f"Failed. Participant ID: {i}, errors counter: {errors}")
            sleep(SLEEP_TIME)
    driver.quit()


def main() -> None:
    # send_messages_by_list()
    # check_replies()


if __name__ == "__main__":
    main()
