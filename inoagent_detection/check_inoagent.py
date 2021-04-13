import re
import csv


def check_single_pattern(text_to_check:str, pattern:str) -> dict:
    """Функция, ищет в тексте упоминание отдельной организации.
    Args:
        text_to_check (str): Текст, который надо проверить, очищенный от тегов.
        pattern (str): Строка с регулярными выражениями.
    Yields:
        result: Возвращает найденные совпадения по одному в формате dictionary.
    """    
    compiled = re.compile(r'{}'.format(pattern), re.IGNORECASE)
    matches = compiled.finditer(text_to_check)
    for match in matches:
        result = {"span":list(match.span()),"text_found": match.group()}            
        yield result


def check_all_patterns(text_to_check:str, extended=False, 
                       patterns_db="patterns_db.csv") -> dict:
    """Функция, которая ищет в тексте упоминание всех организаций из списка.
    Для самого процесса поиска вызывает функцию check_single_pattern.
    Args:
        text_to_check (str): Текст, который надо проверить, очищенный от тегов.
        extended (bool, optional): Применять ли расширенный набор правил. 
        patterns_db (str, optional): Путь к базе данных с информацией. 
    Returns:
        results: Возвращает все найденные совпадения в формате dictionary."""
    with open(patterns_db, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        num_results = 0
        results = {}
        for row in csv_reader:
            info = {"name": row[2], "inoagent_type": row[3], 
            "org_type": row[4], "date": row[5], "excluded": row[6]}
            if extended:
                for result in check_single_pattern(text_to_check, row[0]):
                    result.update(info)
                    results[num_results] = result
                    num_results += 1
            else:
                for result in check_single_pattern(text_to_check, row[1]):
                    result.update(info)
                    results[num_results] = result
                    num_results += 1
    return results
    
    
def main():
    with open("autotest_db/text_to_search.txt", "r", encoding="utf-8") as text_file:
        check_all_patterns(text_file.read())


if __name__ == "__main__":
    main()
