import re
import csv


def check_nko(text_to_check:str, patterns_db="patterns_db.csv"):
    # Детектирование форм одного слова
    # Детектирование словосочетаний
    # Детектирование нескольких словосочетаний одним паттерном
    
    with open(patterns_db) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            compiled = re.compile(r'{}'.format(row[0]))
            matches = compiled.finditer(text_to_check)
            for match in matches:
                result = {"span":list(match.span()), "text_found":match.group(), 
                          "info": row[1] + row[2] + row[3] + row[4] + row[5]}
                print(result)
        

def main():
    text_file = open("text_to_search.txt", "r", encoding="utf-8")
    check_nko(text_file.read()) # all_nko)
    text_file.close()


if __name__ == "__main__":
    main()


##### TO DO ######
# Загрузка регулярок и доп информации из CSV
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
