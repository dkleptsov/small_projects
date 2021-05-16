from time import sleep
from selenium import webdriver


def main():
    # Определяем константы
    WD_PATH = "C:/Program Files (x86)/Chromedriver/chromedriver.exe"
    SMI_URL = "https://minjust.gov.ru/ru/documents/7755/"
    NKO_URL = "http://unro.minjust.ru/NKOForeignAgent.aspx"
    SLEEP_TIME = 2
    
    # Инициализируем драйвер
    driver = webdriver.Chrome(WD_PATH)

    # # Открываем страницу с иноагентами НКО
    # driver.get(NKO_URL)

    # # Выбираем отображение по 500 записей на страницу
    # limit_selector = driver.find_elements_by_class_name("pdg_count")
    # limit_selector[3].click()
    # sleep(SLEEP_TIME)

    # # Нажимаем кнопку поиска
    # search_button = driver.find_element_by_id("b_refresh")
    # search_button.click()
    # sleep(SLEEP_TIME)

    # # Получаем таблицу с иноагентами НКО
    # table = driver.find_element_by_id("pdg")

    # # Сохраняем новую таблицу с иноагентами    
    # # with open("nko_list.txt", "w+", encoding="utf-8") as text_file:
    # #     text_file.write(table.text)
    
    # # Открываем страницу с иноагентами
    # with open("nko_list.txt", "r", encoding="utf-8") as text_file:
    #     old_nko_list = text_file.read()

    # # Сравниваем старый и новый список иноагентов
    # if old_nko_list != table.text:
    #     new_nko = set(table.text.split(sep="\n")).difference(set(old_nko_list.split(sep="\n")))
    # for element in new_nko:
    #     print(element)
        
    # Открываем страницу с иноагентами СМИ
    driver.get(SMI_URL)
    sleep(SLEEP_TIME*3)

    # Получаем таблицу с иноагентами СМИ
    table = driver.find_elements_by_class_name("row-fluid")
    smi_list = table[2].text

    # # Сохраняем новую таблицу с иноагентами    
    # with open("smi_list.txt", "w+", encoding="utf-8") as text_file:
    #     text_file.write(smi_list)
    
    # Открываем страницу с иноагентами
    with open("smi_list.txt", "r", encoding="utf-8") as text_file:
        old_smi_list = text_file.read()
    
    print(old_smi_list == smi_list)

    sleep(SLEEP_TIME)
    driver.quit()


if __name__ == "__main__":
    main()


# docs: https://www.selenium.dev/documentation/en/
# docs: http://bit.ly/webscraping_selenium
