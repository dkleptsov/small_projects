from time import sleep
from selenium import webdriver
from pprint import pprint


def compare_lists(old:str, new:str):
    old_set = set(old.split(sep="\n"))
    new_set = set(new.split(sep="\n"))
    changes = {"added": None, "deleted": None}
    changes["added"] = list(new_set.difference(old_set))
    changes["deleted"] = list(old_set.difference(new_set))
    return changes


def check_new_nko(rewrite:bool = False):
    WD_PATH = "C:/Program Files (x86)/Chromedriver/chromedriver.exe"
    NKO_URL = "http://unro.minjust.ru/NKOForeignAgent.aspx"
    OLD_NKO_PATH = "monitoring/nko_list.txt"
    SLEEP_TIME = 3

    # Инициализируем вебдрайвер и открываем страницу с иноагентами НКО
    # driver = webdriver.Chrome(WD_PATH)
    driver = webdriver.Firefox()
    driver.get(NKO_URL)

    # Выбираем отображение по 500 записей на страницу
    limit_selector = driver.find_elements_by_class_name("pdg_count")
    limit_selector[3].click()
    sleep(SLEEP_TIME)

    # Нажимаем кнопку поиска
    search_button = driver.find_element_by_id("b_refresh")
    search_button.click()
    sleep(SLEEP_TIME)

    # Получаем таблицу с иноагентами НКО
    table = driver.find_element_by_id("pdg")
    new_nko_str = table.text
 
    # Открываем файл со старым списком иноагентов НКО
    with open(OLD_NKO_PATH, "r", encoding="utf-8") as text_file:
        old_nko_str = text_file.read()

    # Сравниваем старый и новый список иноагентов
    nko_changes = compare_lists(old_nko_str, new_nko_str)
    
    # Сохраняем новый список иноагентов НКО в файл
    if rewrite:
        with open(OLD_NKO_PATH, "w+", encoding="utf-8") as text_file:
            text_file.write(new_nko_str)

    driver.quit()    
    return nko_changes


def check_new_smi(rewrite:bool = False):
    WD_PATH = "C:/Program Files (x86)/Chromedriver/chromedriver.exe"
    SMI_URL = "https://minjust.gov.ru/ru/documents/7755/"
    OLD_SMI_PATH = "monitoring/smi_list.txt"
    SLEEP_TIME = 3

    # Инициализируем вебдрайвер и открываем страницу с иноагентами НКО
    # driver = webdriver.Chrome(WD_PATH)
    driver = webdriver.Firefox()
    driver.get(SMI_URL)
    sleep(SLEEP_TIME)

    # Получаем таблицу с иноагентами СМИ
    table = driver.find_elements_by_class_name("row-fluid")
    new_smi_str = table[2].text
    
    # Открываем страницу со старым списком иноагентов СМИ
    with open(OLD_SMI_PATH, "r", encoding="utf-8") as text_file:
        old_smi_str = text_file.read()

    # Сравниваем старый и новый список иноагентов
    smi_changes = compare_lists(old_smi_str, new_smi_str)
  
    # Сохраняем новый список иноагентов НКО в файл
    if rewrite:
        with open(OLD_SMI_PATH, "w+", encoding="utf-8") as text_file:
            text_file.write(new_smi_str)

    driver.quit()    
    return smi_changes


def main():
    pprint(check_new_nko())
    pprint(check_new_smi())


if __name__ == "__main__":
    main()


# docs: https://www.selenium.dev/documentation/en/
# docs: http://bit.ly/webscraping_selenium
