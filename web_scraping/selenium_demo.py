from selenium import webdriver
WD_PATH = "C:/Program Files (x86)/chromedriver.exe"

driver = webdriver.Chrome(WD_PATH)

# http://unro.minjust.ru/NKOForeignAgent.aspx
driver.get("https://minjust.gov.ru/ru/documents/7755/")
print(driver.title)

# search = driver.find_element_by_class_name("table-bordered-wrapper")

search = driver.find_
print(search)
# driver.close()
