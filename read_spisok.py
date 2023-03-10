# Модуль чтения списка
from pprint import pprint


def reading_spisok() -> list:
    """Функция чтения файла с поисковыми запросами"""

    spisok = []

    with open('spisok.txt', 'r') as file:
        for line in file:
            spisok.append(line[:-1])

    spisok = set(spisok)  # отсекание дублей на всякий случай
    spisok = sorted(tuple(spisok))  # список с данными отсортированный
    return spisok


if __name__ == '__main__':
    pprint(reading_spisok())
