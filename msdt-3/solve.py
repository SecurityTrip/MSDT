import re
import csv
from checksum import calculate_checksum, serialize_result

# Регулярные выражения для проверки данных
regular_expressions = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'height': r'^[1-2]\.\d{2}$',
    'snils': r'^\d{11}$',
    'passport': r'^\d{2} \d{2} \d{6}$',
    'occupation': r'^[A-Za-zА-Яа-яёЁ\s-]+$',
    'longitude': r'^-?(180|(\d{1,2}|1[0-7]\d)(\.\d{1,})?)$',
    'hex_color': r'^#[0-9a-fA-F]{6}$',
    'issn': r'^\d{4}-\d{4}$',
    'locale_code': r'^[a-zA-Z]+(-[a-zA-Z]+)*$',
    'time': r'^[0-2]\d:[0-5]\d:[0-5]\d(\.\d{1,6})?$'
}


def check_row(row):
    """
    Проверка строки на соответствие всем правилам.
    """
    for key, expression in regular_expressions.items():
        if not re.match(expression, row[key]):
            print(f"Error in field {key}: {row[key]}")
            return False
    return True


def check_file():
    """
    Проверка всех строк файла и возврат списка некорректных строк.
    """
    invalid_rows = []
    with open('75.csv', newline='', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        for index, row in enumerate(reader):
            if not check_row(row):
                invalid_rows.append(index)
        print(len(invalid_rows))
    return invalid_rows


variant = 75
invalid_rows = check_file()
checksum = calculate_checksum(invalid_rows)
serialize_result(variant, checksum)
