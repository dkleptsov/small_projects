import sys
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from pprint import pprint


NKO_URL = "http://unro.minjust.ru/NKOForeignAgent.aspx"
OLD_NKO_PATH = "monitoring/nko_list.txt"

SMI_URL = "https://minjust.gov.ru/ru/documents/7755/"
SMI_XPATH = "/html/body/main/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/table/tbody"
OLD_SMI_PATH = "monitoring/smi_list.txt"

EO_URL = "https://minjust.gov.ru/ru/documents/7822/"
EO_XPATH = "/html/body/main/div[3]/div/div[1]/div[1]/div[2]/div"
OLD_EO_PATH = "monitoring/eo_list.txt"

TO_URL = "http://www.fsb.ru/fsb/npd/terror.htm"
TO_XPATH = "/html/body/section/div[1]/div[2]/div[2]/div/div[3]/div/table/tbody"
OLD_TO_PATH = "monitoring/to_list.txt"

NO_URL = "https://minjust.gov.ru/ru/documents/7756/"
NO_XPATH = "/html/body/main/div[3]/div/div[1]/div[1]/div[2]/div/div/table"
OLD_NO_PATH = "monitoring/no_list.txt"

SLEEP_TIME = 5


def get_new_str(url:str, xpath:str) -> str:
    # Инициализируем вебдрайвер и открываем страницу
    if sys.platform != "win32":
        display = Display(visible=0, size=(128, 96))  
        display.start()
    driver = webdriver.Firefox()
    driver.implicitly_wait(SLEEP_TIME)
    # Получаем изменения
    try:
        driver.get(url)
        sleep(SLEEP_TIME)
        table = driver.find_element_by_xpath(xpath)
        new_str = table.text
    except:
        new_str = None

    # Закрываем драйвер и дисплей
    driver.quit()
    if sys.platform != "win32":
        display.stop()
    
    return new_str


def compare_lists(old:str, new:str) -> tuple:
    old_set = set(old.split(sep="\n"))
    new_set = set(new.split(sep="\n"))
    added = list(new_set.difference(old_set))
    deleted = list(old_set.difference(new_set))
    return added, deleted, True


def get_changes(new_str:str, old_str_path:str, rewrite:bool) -> tuple:
    if new_str is None:
        return ([], [], False)

    # Открываем страницу со старым списком
    with open(old_str_path, "r", encoding="utf-8") as text_file:
        old_str = text_file.read()

    # Сравниваем старый и новый список
    changes = compare_lists(old_str, new_str)
  
    # Сохраняем новый список
    if rewrite:
        with open(old_str_path, "w+", encoding="utf-8") as text_file:
            text_file.write(new_str)
    return changes


def check_new_nko(rewrite:bool = False) -> tuple:
    # Инициализируем вебдрайвер и открываем страницу с иноагентами НКО
    if sys.platform != "win32":
        display = Display(visible=0, size=(128, 96))  
        display.start()
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    try:
        driver.get(NKO_URL)
        sleep(SLEEP_TIME)

        # Выбираем отображение по 500 записей на страницу
        limit_selector = driver.find_elements_by_class_name("pdg_count")
        limit_selector[3].click()
        sleep(SLEEP_TIME)

        # Нажимаем кнопку поиска
        search_button = driver.find_element_by_id("b_refresh")
        search_button.click()
        sleep(SLEEP_TIME)

        # Получаем изменения
        table = driver.find_element_by_id("pdg")
        new_nko_str = table.text
        nko_changes = get_changes(new_nko_str, OLD_NKO_PATH, rewrite)
    except:
        nko_changes = ([], [], False)

    # Закрываем драйвер и дисплей
    driver.quit()
    if sys.platform != "win32":
        display.stop()
    return nko_changes


def check_new_smi(rewrite:bool = False) -> tuple:
    new_str = get_new_str(SMI_URL, SMI_XPATH)
    changes = get_changes(new_str, OLD_SMI_PATH, rewrite)
    return changes


def check_new_eo(rewrite:bool = False) -> tuple:
    new_str = get_new_str(EO_URL, EO_XPATH)
    changes = get_changes(new_str, OLD_EO_PATH, rewrite)
    return changes


def check_new_to(rewrite:bool = False) -> tuple:
    new_str = get_new_str(TO_URL, TO_XPATH)
    changes = get_changes(new_str, OLD_TO_PATH, rewrite)
    return changes


def check_new_no(rewrite:bool = False) -> tuple:
    new_str = get_new_str(NO_URL, NO_XPATH)
    changes = get_changes(new_str, OLD_NO_PATH, rewrite)
    return changes


def check_all_orgs(rewrite:bool = False) -> tuple:
    changes_str, orgs_list, download_success_list = "", [], []
    orgs_list.append([check_new_nko(rewrite), "иноагентов НКО", NKO_URL])
    orgs_list.append([check_new_smi(rewrite), "иноагентов СМИ", SMI_URL])
    orgs_list.append([check_new_eo(rewrite), "экстремистских организаций",
    EO_URL])
    orgs_list.append([check_new_to(rewrite), "террористических организаций",
    TO_URL])
    orgs_list.append([check_new_no(rewrite), "нежелательных организаций", 
    NO_URL])

    for (added, deleted, download_success), name, url in orgs_list:
        if added and download_success:
            changes_str += f"\n✔️ В список {name} добавлено:\n{added}\n"
        if deleted and download_success:
            changes_str += f"\n❌ Из списка {name} удалено:\n{deleted}\n"
        if download_success and added or deleted:
            changes_str += f"\n🔗 Ссылка на список для проверки: {url}\n\n"
        download_success_list.append(download_success)
    return changes_str, download_success_list


def main():
    # pprint(check_new_nko(rewrite=False))
    # pprint(check_new_smi(rewrite=False))
    # pprint(check_new_eo(rewrite=False))
    # pprint(check_new_to(rewrite=False))
    # pprint(check_new_no(rewrite=False))
    pprint(check_all_orgs(rewrite=False))
    pass


if __name__ == "__main__":
    main()
