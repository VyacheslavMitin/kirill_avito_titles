import os
import time
from bs4 import BeautifulSoup as BS
from selenium import webdriver

from read_spisok import reading_spisok

# Константы
PATH_OUTPUT = 'output'  # путь к каталогу с получившимися файлами


# Функции
def making_dir_output():
    """Функция создания каталогов для получающихся файлов"""
    os.makedirs(PATH_OUTPUT, exist_ok=True)


def parsing_titles(request):
    """Функция парсинга заголовков объявлений"""

    making_dir_output()  # создание необходимых каталогов

    list = []
    url = f"https://www.avito.ru/ulyanovsk?q={request}"

    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url)
    time.sleep(0)  # было 5, не помню зачем ждать 5 секунд, возможно для запуска хрома

    for i in range(20):  # 20 раз скроллим вниз страницу
        driver.execute_script("window.scrollBy(0,1000)", "")
        time.sleep(0)  # Было 1, можно 0.1, пауза между скроллами страницы, нужно если страница прогруж. при скроллинге

    html = driver.page_source
    soup = BS(html, "html.parser")
    title_names = soup.find_all(itemprop="name")

    for i in title_names:
        if i:
            list.append(i.text.strip())

    list_set = set(list)

    for item in list_set:
        with open(f'{PATH_OUTPUT}/{request}.txt', 'a') as file:
            file.write(item)
            file.write('\n')
    driver.close()


if __name__ == '__main__':
    for item in reading_spisok():
        parsing_titles(item)
