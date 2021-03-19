import re
import csv
import pyforest
from datetime import datetime
import time


def check_single_pattern(text_to_check:str, pattern:str, name="pass", inoagent_type="pass",
                         org_type="pass", date="pass", excluded="pass", verbose=True):
    """
    Функция, ищет в тексте упоминание отдельной организации.

    Args:
        text_to_check (str): Текст, который надо проверить, очищенный от тегов.
        pattern (str): Строка с регулярными выражениями.
        name (str): Название организации
        inoagent_type (str): Тип организации иноагента: СМИ или НКО.
        org_type (str): Организационная форма: юридическое или физическое лицо.
        date (str): Дата внесения организации в реестр.
        excluded (str): Исключена ли организация из реестра.
        verbose (bool): Флаг печатать ли информацию в консоль, нужен для отладки. По умолчанию False.

    Yields:
        result: Возвращает найденные совпадения по одному в формате dictionary.
    """    
    compiled = re.compile(r'{}'.format(pattern), re.IGNORECASE) # Протестировать работу
    matches = compiled.finditer(text_to_check)
    for match in matches:
        result = {"span":list(match.span()), "text_found": match.group(), "name": name,
                  "inoagent_type": inoagent_type, "org_type": org_type, "date": date, "excluded": excluded}
        if verbose:
            print(result["text_found"], result["name"])
            now_string = datetime.now().strftime("%d_%m_%Y_%H")
            with open("logs/log_{}.txt".format(now_string), "a", encoding="utf-8") as log:
                log.write(result["text_found"] + " " + result["name"] + "\n")
            
        yield result


def check_all_patterns(text_to_check:str, extended=False, patterns_db="patterns_db.csv", verbose=False):
    """
    Функция, которая ищет в тексте упоминание всех организаций из списка.
    Для самого процесса поиска вызывает функцию check_single_pattern.

    Args:
        text_to_check (str): Текст, который надо проверить, очищенный от тегов.
        extended (bool, optional): Применять ли расширенный набор правил. По умолчанию False.
        patterns_db (str, optional): Путь к базе данных с информацией. По умолчанию "patterns_db.csv".
        verbose (bool, optional): Флаг печатать ли информацию в консоль, нужен для отладки. По умолчанию False.

    Returns:
        results: Возвращает все найденные совпадения в формате dictionary.
    """
        
    with open(patterns_db, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        num_results = 0
        results = {}
        for row in csv_reader:
            if extended:
                for result in check_single_pattern(text_to_check, row[0], row[2], row[3], row[4], row[5], row[6], verbose):
                    results[num_results] = result
                    num_results += 1
            else:
                for result in check_single_pattern(text_to_check, row[1], row[2], row[3], row[4], row[5], row[6], verbose):
                    results[num_results] = result
                    num_results += 1
    if verbose and len(results) > 0:
        print('Total number of results: {}'.format(len(results)))
    return results


def check_lenta(file_path):
    """Функция, которая ищет названия иностранных агентов в базе данных новостей lenta.ru

    Args:
        file_path (str): путь до файла с базой новостей lenta.ru
    """    
    with open(file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            results = check_all_patterns(row[2])
            if len(results) > 0:
                for i in range(len(results)):
                    print("Мы нашли текст: {}".format(results[i]["text_found"]))
                    print("Название иноагента: {}".format(results[i]["name"]))
                    print("Правовая форма иноагента: {}".format(results[i]["org_type"]))
                    print("Дата включения в реестр: {}".format(results[i]["date"]))
                    print("Заголовок статьи: {}".format(row[1]))
                    print("Ссылка на статью: {}".format(row[0]))
                    input("Нажмите Enter для продолжения...")
                          

def add_news(new_db_path:str, old_db_path:str, conact_db_path:str):
    """Функция для добавления свежих новостей в базу.
    Не протестирована. В идеале надо удалять дубликаты еще.

    Args:
        new_db_path (str): путь к файлу с новыми новостями.
        old_db_path (str): путь к файлу со старыми новостями
        conact_db_path (str): путь к объединенному файлу, который будет создан
    """    
    column_names = ['url', 'title', 'text', 'topic', 'tags', 'date']
    new_db = pd.read_csv(new_db_path, names=column_names)
    old_db = pd.read_csv(old_db_path)

    print(new_db)
    print(old_db)
    
    df = pd.concat([old_db, new_db]).reset_index(drop=True)
    print(df.head())
    print(df.tail())
    
    df.to_csv(conact_db_path, index=False)
    

def reverse_df(original:str, reversed:str):
    """Функция для изменения порядка новостей.
    Кажется более логичным обращать базу на лету, чтобы сэкономить место на диске.

    Args:
        original (str): путь к оригинальному файлу
        reversed (str): путь к файлу с обратной сортировкой, который будет создан
    """
    column_names = ['url', 'title', 'text', 'topic', 'tags', 'date']
    df = pd.read_csv(original)
    print("База до изменения порядка: ")
    print(df)
    df = df.reindex(index=df.index[::-1])
    print("База после изменения порядка: ")
    print(df)
    df.to_csv(reversed, index=False)
    

def test_single_pattern(number_to_test:int, patterns_db="patterns_db.csv", 
                        lenta_path="D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv", extended = False):
    """Функция для тестирования паттернов для детекции отдельного иноагента.

    Args:
        number_to_test (int): номер регулярного выражения, которое надо протестировать.
    """
    with open("text_to_search.txt", encoding="utf-8") as text_file:
        nko_list = text_file.read()
    
    with open(patterns_db, encoding="utf-8") as csv_file:
        pattern = list(csv.reader(csv_file, delimiter=';'))[number_to_test]
        print("\nНазвание иноагента: {}".format(pattern[2]))
        if extended:
            pattern_to_test = pattern[0]
            print("Тестирование расширенного режима")
        else:
            pattern_to_test = pattern[1]
            print("Тестирование обычного режима")

        print("\n1. Поиск по списку иноагентов:")
        results = [x for x in check_single_pattern(nko_list, pattern_to_test, name=pattern[2])]

        print("\n2. Поиск по новостям lenta.ru:")
        with open(lenta_path, encoding="utf-8") as csv_file:
            lenta = csv.reader(csv_file, delimiter=',')
            for news in lenta:
                results = [x for x in check_single_pattern(news[2], pattern_to_test, name=news[0])]
    
    
def main():
    # add_news("D:/OneDrive/data/lenta_check/lenta_latest.csv", 
    #          "D:/OneDrive/data/lenta_check/lenta_030821.csv",
    #          "D:/OneDrive/data/lenta_check/lenta_130821.csv")
   
    # reverse_df("D:/OneDrive/data/lenta_check/lenta_130821.csv",
    #            "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv")
    
    # LENTA_PATH = 'D:/OneDrive/data/lenta_check/lenta_recent_reversed.csv'
    # check_lenta(LENTA_PATH)
    
    start = time.time()
    for i in range(93,94):
        print("\n************\ni = {}, номер строки = {}".format(i, i+1))
        test_single_pattern(i)
        time.sleep(20)
    
    print("Проверка заняла: {0:.2f} секунд".format(time.time() - start))
    
    # test_single_pattern(7, extended = False)
    
if __name__ == "__main__":
    main()

