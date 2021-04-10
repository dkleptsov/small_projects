# Посмотреть методы объекта:
print(dir({}))


# def check_lenta(file_path):
#     """Функция, которая ищет названия иностранных агентов в базе данных новостей lenta.ru

#     Args:
#         file_path (str): путь до файла с базой новостей lenta.ru
#     """    
#     with open(file_path, encoding="utf-8") as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         for row in csv_reader:
#             results = check_all_patterns(row[2])
#             if len(results) > 0:
#                 for i in range(len(results)):
#                     print("Мы нашли текст: {}".format(results[i]["text_found"]))
#                     print("Название иноагента: {}".format(results[i]["name"]))
#                     print("Правовая форма иноагента: {}".format(results[i]["org_type"]))
#                     print("Дата включения в реестр: {}".format(results[i]["date"]))
#                     print("Заголовок статьи: {}".format(row[1]))
#                     print("Ссылка на статью: {}".format(row[0]))
#                     input("Нажмите Enter для продолжения...")
                          

# def add_news(new_db_path:str, old_db_path:str, conact_db_path:str):
#     """Функция для добавления свежих новостей в базу.
#     Не протестирована. В идеале надо удалять дубликаты еще.

#     Args:
#         new_db_path (str): путь к файлу с новыми новостями.
#         old_db_path (str): путь к файлу со старыми новостями
#         conact_db_path (str): путь к объединенному файлу, который будет создан
#     """    
#     column_names = ['url', 'title', 'text', 'topic', 'tags', 'date']
#     new_db = pd.read_csv(new_db_path, names=column_names)
#     old_db = pd.read_csv(old_db_path)

#     print(new_db)
#     print(old_db)
    
#     df = pd.concat([old_db, new_db]).reset_index(drop=True)
#     print(df.head())
#     print(df.tail())
    
#     df.to_csv(conact_db_path, index=False)
    

# def reverse_df(original:str, reversed:str):
#     """Функция для изменения порядка новостей.
#     Кажется более логичным обращать базу на лету, чтобы сэкономить место на диске.

#     Args:
#         original (str): путь к оригинальному файлу
#         reversed (str): путь к файлу с обратной сортировкой, который будет создан
#     """
#     column_names = ['url', 'title', 'text', 'topic', 'tags', 'date']
#     df = pd.read_csv(original)
#     print("База до изменения порядка: ")
#     print(df)
#     df = df.reindex(index=df.index[::-1])
#     print("База после изменения порядка: ")
#     print(df)
#     df.to_csv(reversed, index=False)
    

# def check_single_pattern_on_lenta(number_to_test:int, patterns_db="patterns_db.csv", 
#                         lenta_path="D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv", extended = False):
#     """Функция для тестирования паттернов для детекции отдельного иноагента.

#     Args:
#         number_to_test (int): номер регулярного выражения, которое надо протестировать.
#     """
#     with open("text_to_search.txt", encoding="utf-8") as text_file:
#         nko_list = text_file.read()
    
#     with open(patterns_db, encoding="utf-8") as csv_file:
#         pattern = list(csv.reader(csv_file, delimiter=';'))[number_to_test]
#         print("\nНазвание иноагента: {}".format(pattern[2]))
#         if extended:
#             pattern_to_test = pattern[0]
#             print("Тестирование расширенного режима")
#         else:
#             pattern_to_test = pattern[1]
#             print("Тестирование обычного режима")

#         print("\n1. Поиск по списку иноагентов:")
#         results = [x for x in check_single_pattern(nko_list, pattern_to_test, name=pattern[2])]

#         print("\n2. Поиск по новостям lenta.ru:")
#         with open(lenta_path, encoding="utf-8") as csv_file:
#             lenta = csv.reader(csv_file, delimiter=',')
#             for news in lenta:
#                 results = [x for x in check_single_pattern(news[2], pattern_to_test, name=news[0])]

# # add_news("D:/OneDrive/data/lenta_check/lenta_latest.csv", 
# #          "D:/OneDrive/data/lenta_check/lenta_030821.csv",
# #          "D:/OneDrive/data/lenta_check/lenta_130821.csv")

# # reverse_df("D:/OneDrive/data/lenta_check/lenta_130821.csv",
# #            "D:/OneDrive/data/lenta_check/lenta_130821_reversed.csv")

# # LENTA_PATH = 'D:/OneDrive/data/lenta_check/lenta_recent_reversed.csv'
# # check_lenta(LENTA_PATH)

# start = time.time()
# for i in range(93,94):
#     print("\n************\ni = {}, номер строки = {}".format(i, i+1))
#     check_single_pattern_on_lenta(i, extended = False)
#     time.sleep(20)

# print("Проверка заняла: {0:.2f} секунд".format(time.time() - start))