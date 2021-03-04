import re
import csv


def re_check(text_to_check:str, pattern:str, name:str, nko_type:str, org_type:str, date:str, excluded:str):
    # ! Не делать текст lower, а использовать игноркейс  (re.IGNORECASE или нарезать оригинальный текст)
    # ! Сокращенная и ласкательная форма имен Люда и т.д. Решение: сократить до части, которая не меняется Люд
    # ! Надо ли ставить знак ? перед несколькими регулярками
    # ? Детектирование словосочетаний
    # ? Детектирование нескольких словосочетаний одним паттерном
    # Детектирование организаций
    # Придумать паттерны для extended режима
    lowered_text = text_to_check.lower()
    compiled = re.compile(r'{}'.format(pattern, re.IGNORECASE))
    matches = compiled.finditer(lowered_text)
    result = {}
    for i, match in enumerate(list(matches)):
        print(i)
        print(X)
        # result [i] = {"span":list(match.span()), "text_found": text_to_check[match.start(): match.end()], 
        #             "name": name, "nko_type": nko_type, "org_type": org_type, "date": date, "excluded": excluded}
    
    # return result
    

def check_nko(text_to_check:str, extended=False, patterns_db="patterns_db.csv"):
    with open(patterns_db) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if extended:
                return re_check(text_to_check, row[0], row[2], row[3], row[4], row[5], row[6])
            else:
                return re_check(text_to_check, row[1], row[2], row[3], row[4], row[5], row[6])
                 

def main():
    text_file = open("text_to_search.txt", "r", encoding="utf-8")
    print(check_nko(text_file.read()))
    text_file.close()


if __name__ == "__main__":
    main()


##### TO DO ######
# Сделать правила для физлиц
# Сделать правила для юрлиц
# Очистка текста от мусора? (удалять все не буквы? А как возвращать результаты? Есть ли цифры?)
# Проверка на нулевые значения
# Загружать тест для проверки из файла
# Развертывание на линуксе (батник для линукса)
# Написать тесты
# Статик метод?
# Документация к функциям
# Веб сервис
# Очищение от веб-тегов
