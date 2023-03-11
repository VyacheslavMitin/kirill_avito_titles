# Модуль чтения списка


def reading_lists(file) -> list:
    """Функция чтения файла с поисковыми запросами"""

    spisok = []

    with open(f'{file}.txt', 'r', encoding="utf-8") as file:
        for line in file:
            spisok.append(line[:-1])

    spisok = set(spisok)  # отсекание дублей на всякий случай
    spisok = sorted(tuple(spisok))  # список с данными отсортированный
    return spisok


if __name__ == '__main__':
    from pprint import pprint
    print("Товары")
    pprint(reading_lists('goods'))
    print("\nГорода")
    pprint(reading_lists('cities'))
