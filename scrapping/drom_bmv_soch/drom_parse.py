import json
import os
from bs4 import BeautifulSoup
import requests

"""Создаем файл для записи ошибок"""
if os.path.exists("err.log"):
    os.remove("err.log")

"""Создаем новый лог"""
with open("err.log", 'w+') as file:
    file.read()

"""Переходим на страничку категорий для бмв"""
url = "https://sochi.drom.ru/bmw/?grouping=1"
try:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    """смотрим сколько страниц для категорий"""
    lists_category = soup.find(class_ = "css-1d1vsky e1lm3vns0").find_all("div")
    count_lists_category = len(lists_category)
except Exception as ex:
    with open("err.log", 'a') as file:
        file.write(f'Ошибка при получении количества листов категорий, {ex} \n')

"""Проверяем наличие директории для файлов"""
if not os.path.exists('files'):
    os.mkdir('files')

"""Словарь категория - ссылка"""
all_category_href_dict = {}

"""проходимся по всем страницам для поиска категорий, подставляя в гет запрос номер страницы"""
for num_page_category in range(1, count_lists_category + 1):
    # if num_page_category == 1:
    url = f"https://sochi.drom.ru/bmw/page{num_page_category}/?grouping=1"
    req = requests.get(url)
    # soup = BeautifulSoup(req.text, "lxml")
    try:
        with open(os.path.join(f'files/category{num_page_category}.html'), 'w', encoding='utf-8') as file:
            file.write(req.text)
    except Exception as ex:
        with open("err.log", 'a') as file:
            file.write(f'Не удалось записать страницу по адресу {url}\n')

    with open(os.path.join(f'files/category{num_page_category}.html'), 'r', encoding='utf-8') as file:
            text_page_category = file.read()

    """Передаем текст страницы категории в объект супа"""
    soup = BeautifulSoup(text_page_category, "lxml")

    """Поиск категорий авто на странице"""
    all_categories_on_page = soup.find("div", class_ = "css-flpniz")
    elements_category = all_categories_on_page.find_all(class_ = "css-nox51k e1dg5km75")
    for category in elements_category:
        """Забираем первое значние из опиания как название категории"""
        list_val = category.text.split(',')
        name_category = list_val[0]
        """Заполняем словарь категорий"""
        all_category_href_dict[name_category] = category.get("href")

"""Записываем в файл все наименования категорий и ссылки на них"""
with open(os.path.join(f'files/all_category_href.html'), 'w', encoding='utf-8') as file:
    for key, val in all_category_href_dict.items():
        file.write(f'{key} : {val} \n')

"""Проверяем наличие папки для категорий, если нет создаем"""
path_directory = os.path.join('files')

"""Проверяем наличие директории для файлов"""
try:
    if os.path.exists(os.path.join(os.path.abspath(path_directory), 'category')):
        pass
    else:
        os.mkdir(os.path.join(os.path.abspath(path_directory), 'category'))
    path_category = os.path.join(os.path.abspath(path_directory), 'category')
except Exception as ex:
    print('Ошибка при попытке создать папки категория')
    print(ex)

"""Перебираем категории"""
for key, val in all_category_href_dict.items():
    """Создаем директории для файлов json по категориям авто"""
    if not os.path.exists(os.path.join(path_directory, f'{key[4:]}')):
        os.mkdir(os.path.join(path_directory, f'{key[4:]}'))

    # if key == 'BMW 3-Series':
    url = val
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")
    """смотрим сколько страниц в этой категории'"""
    lists_cars = soup.find(class_ = "css-14wh0pm e1lm3vns0").find_all("div")
    count_lists_cars = len(lists_cars)

    """Пробегаемся по страничкам с автомобилями, так как в гет запросе название марки не используется, обрезаем его"""
    try:
        all_cars_list = []
        for cars_page_num in range(1, count_lists_cars + 1):
            url = f'https://sochi.drom.ru/bmw/{key[4:].lower()}/page{cars_page_num}/'
            req = requests.get(url)
            soup = BeautifulSoup(req.text, "lxml")

            """Все автомобили на странице"""
            cars_greed = soup.find(class_ = "css-1nvf6xk eaczv700")
            all_cars = cars_greed.find_all(class_ = "css-xb5nz8 ewrty961")
            """Наполняем список ссылок на автомобили со страницы"""
            for car in all_cars:
                all_cars_list.append(car.get("href"))
    except Exception as ex:
        print(ex)

    count_all_cars_list = len(all_cars_list)
    schet_count_all_cars_list = count_all_cars_list

    """Проверяем наличие файла с данными в директории, елси есть - удаляем"""
    if os.path.exists(os.path.join(path_directory, f'{key[4:]}/{key[4:]}.json')):
        os.remove(os.path.join(path_directory, f'{key[4:]}/{key[4:]}.json'))

    """Пробегаемся по всем автомобилям на странице"""
    for car_link in all_cars_list:

        url = car_link
        req_text = requests.get(url).text

        """Обрабатываем записи и записывам в словарь данные"""
        soup = BeautifulSoup(req_text, "lxml")
        attributes = soup.find_all(class_ ="css-11ylakv ezjvm5n0")
        attributes_dict = {}

        name_ad = soup.find("span", class_ = "css-1kb7l9z e162wx9x0").text
        price = soup.find("div", class_ = "css-eazmxc e162wx9x0").text.replace('\xa0', '')

        attributes_dict["name_ad"] = name_ad
        attributes_dict["price"] = price

        for attribute in attributes:
            """Обрабатываем параметры, удаляем лишние символы"""
            name_attribute = attribute.find("th").text
            val_attribute = attribute.find("td").text
            val_attribute = val_attribute.replace(' ', '')

            if name_attribute == 'Мощность':
                val_attribute = val_attribute.replace(', налог', '')

            attributes_dict[name_attribute] = val_attribute

        with open(os.path.join(path_directory, f'{key[4:]}/{key[4:]}.json'), 'a', encoding='utf-8') as file:
            json.dump(attributes_dict, file, indent = 4, ensure_ascii = False)

        schet_count_all_cars_list -= 1
        print(f'Записаны данные из категории {key[4:]} по автомобилю {count_all_cars_list - schet_count_all_cars_list}, осталось {schet_count_all_cars_list}')


print('Работа завершена')
