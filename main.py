import os
import time
from datetime import datetime

from bs4 import BeautifulSoup as BS
from selenium import webdriver

from read_files import reading_lists

# Константы
NOW_DATE_TIME = datetime.now().strftime('%d.%m.%Y_%H-%M-%S')

# Переменные
PATH_OUTPUT = f'output_{NOW_DATE_TIME}_'  # путь к каталогу с получившимися файлами


# Функции
def making_dir_output(path):
    """Функция создания каталогов для получающихся файлов"""
    os.makedirs(path, exist_ok=True)


def parsing_titles(location, request, page=1):
    """Функция парсинга заголовков объявлений"""

    path_output = PATH_OUTPUT + location
    making_dir_output(path_output)  # создание необходимых каталогов

    list_ = []
    url = f"https://www.avito.ru/{location}?p={page}&q={request}"
    # https://www.avito.ru/moskva?p=1&q=Кухня

    driver = webdriver.Chrome(executable_path='chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("log-level=3")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(0)  # было 5, не помню зачем ждать 5 секунд, возможно для запуска хрома

    for i in range(20):  # 20 раз скроллим вниз страницу
        driver.execute_script("window.scrollBy(0,1000)", "")
        time.sleep(0)  # Было 1, можно 0.1, пауза между скроллами страницы, нужно если страница прогруж. при скроллинге

    html = driver.page_source
    soup = BS(html, "html.parser")
    title_names = soup.find_all(itemprop="name")

    driver.get(f"https://www.avito.ru/{location}?p=2&q={request}")

    for i in range(20):  # 20 раз скроллим вниз страницу
        driver.execute_script("window.scrollBy(0,1000)", "")
        time.sleep(0)  # Было 1, можно 0.1, пауза между скроллами страницы, нужно если страница прогруж. при скроллинге

    html = driver.page_source
    soup = BS(html, "html.parser")
    title_names2 = soup.find_all(itemprop="name")

    for i in title_names:
        if i:
            list_.append(i.text.strip())

    for i in title_names2:
        if i:
            list_.append(i.text.strip())

    list_set = set(list_)
    list_set = sorted(list_set)

    print(f"~ {datetime.now().strftime('%d.%m.%Y || %H:%M:%S')} ~ Создание файла с городом '{location.upper()}' "
          f"и поиском '{request.upper()}'")
    for i in list_set:
        with open(f'{path_output}/{request.title()}.txt', 'a', encoding="utf-8") as file:
            file.write(i)
            file.write('\n')
    driver.close()


def main():
    """Основная функция"""
    start_time = datetime.now()

    print(f"Скрипт сбора заголовков запущен {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")

    for city in reading_lists('cities'):
        for good in reading_lists('goods'):
            parsing_titles(city, good)

    print(f"\nЗавершено {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")

    finish_time = datetime.now() - start_time
    finish_time = str(finish_time)[:-7]  # обрезание хвоста с мили секундами
    print(f"Выполнено за {finish_time}")


if __name__ == '__main__':
    main()
