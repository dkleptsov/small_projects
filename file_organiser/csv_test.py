import csv

f = open('new_onedrive.csv', 'w')
with f:
    writer = csv.DictWriter(f, fieldnames=['fname', 'hash', 'path'])
    writer.writeheader()  # надо писать один раз
    # writer.writerow({'min': 'John', 'max': 'Smith'})

f.close()

# f = open('file_list.csv', 'r')
# with f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         print(row)
# f.close()


# Docs: http://zetcode.com/python/csv/
# Docs: https://docs.python.org/3/library/csv.html
