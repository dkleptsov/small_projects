import re
import csv


def check_single_pattern(text_to_check:str, pattern:str, name:str, inoagent_type:str, org_type:str, date:str, excluded:str, verbose:bool):
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
    
    compiled = re.compile(r'{}'.format(pattern), re.IGNORECASE)
    matches = compiled.finditer(text_to_check)
    for match in matches:
        result = {"span":list(match.span()), "text_found": match.group(), "name": name,
                  "inoagent_type": inoagent_type, "org_type": org_type, "date": date, "excluded": excluded}
        if verbose:
            print(result["text_found"], result["span"], result["name"])
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
                          

def main():
    LENTA_PATH = 'lenta.csv'
    check_lenta(LENTA_PATH)
    

if __name__ == "__main__":
    main()

