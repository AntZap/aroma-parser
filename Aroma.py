# импорт библиотек
import json

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
from fake_useragent import UserAgent


def parser_aroma(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.2.765 Yowser/2.5 Safari/537.36"
    }

    # req = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    # print(req.status_code)
    #browser = webdriver.Chrome()
    # запускаем первоначальную ссылку, кликаем по кнопке Ароматы, скролим до кнопки показать еще и выгружаем данные
    #browser.get(url=url)
    #time.sleep(3)

    # share = browser.find_element(By.LINK_TEXT, "Ароматы")
    # share.click()
    # time.sleep(3)
    # button = browser.find_element(By.XPATH, "//div[@class='js-store-load-more-btn t-store__load-more-btn t-btn t-btn_sm']")  # показал див и класс по которому найти кнопку и нажать загрузить еще
    # button.location_once_scrolled_into_view
    # button.click()
    # time.sleep(3)
    # выгруженные данные записываем в файл

    # with open('aroma.html', 'w', encoding='utf-8') as file:  # запись страницы в файл
    #    file.write(browser.page_source)

    # share1 = browser.find_element(By.LINK_TEXT, "Красители")
    # share1.click()
    # time.sleep(3)

    # with open('kras.html', 'w', encoding='utf-8') as file:  # запись страницы в файл
    #    file.write(browser.page_source)

    with open('aroma.html', encoding='utf-8') as file:  # открытие страницу с ароматами из файла
       src = file.read()
       soup = bs(src, "lxml")

    with open('kras.html', encoding='utf-8') as file:  # открытие страницу с ароматами из файла
        src1 = file.read()
        soup1 = bs(src1, "lxml")

    # ищем в строках сайта название аромата и информацию про них
    aroma_names = soup.find_all('div', class_="t-store__card__wrap_all")
    kras_names = soup1.find_all('div', class_="t-store__card__wrap_all")

    project_urls = []
    kras_urls = []
    for name in aroma_names:  # находим в каждом названии аромата ссылку для перехода внутрь для полной информации
        project_url = name.find("a").get("href")
        project_urls.append(project_url)

    for kras1 in kras_names:  # находим в каждом названии красителя ссылку для перехода внутрь для полной информации

        kras_url = kras1.find("a").get("href")
        kras_urls.append(kras_url)
        #print(kras_url)
    # Добавляем в список название, описание и ноты, путем посещения каждой ссылки аромата и выгрузки из нее данных при помощи цикла
    list_aroma = []

    for project_url in project_urls:
        req = requests.get(project_url, headers={'User-Agent': UserAgent().chrome})
        project_name = project_url.split("/")[-1]
        if project_name == "":
            project_name = project_url.split("/")[-2]

        # with open (f'aroma/{project_name}.html', 'w', encoding='utf-8') as file: #запись страниц с ароматами в файлы
        #     file.write(req.text)

        with open(f'aroma/{project_name}.html', encoding='utf-8') as file:  # открытие страницы с ароматами из файла
            src = file.read()
            soup = bs(src, "lxml")

        aroma_names1 = soup.find('title').text.replace("Greenwax — Ароматизатор для свечей ","")  # заменяем рекламу на пустой символ, чтобы исключить из названия и оставить только аромат
        aroma_opisanie = soup.find('div', class_="t744__descr t-descr t-descr_xxs").text  # находим данные описания

        aroma_not = soup.find_all("div", class_="tn-atom")  # находим данные нот и затем исключаем ненужную информацию, которая в списке list и оставляем только ноты и интенсивность при помощи цикла
        aroma_nots = []
        list = ['Ноты', 'Нагрузка для свечей', 'Нагрузка для диффузоров',
                'Синтезированные ароматизаторы с добавлением эфирных масел и душистых веществ органического происхождения ',
               'Ароматизаторы произведены по формуле, разработанной специально для использования в свечах',
               'Разработан в США',
               'Рецептура американской компании согласно международным стандартам безопасности IFRA и REACH',
               'Примечание: Ароматизаторы разливаются по весу в граммах. Из-за разной плотности уровень жидкости в флаконах может различаться',
               '  При попадании воды в ходе эксплуатации ароматизатор в смеси с Augeo склонен к расслоению',
               'Примечание: Ароматизаторы разливаются по весу в граммах. Из-за разной плотности уровень жидкости в флаконах может различаться',
               '', 'Интенсивность', 'Содержит эфирные масла',
               '  Испытания на рекомендуемую нагрузку проводились на базе для диффузоров — Augeo',
               'Примечание: из-за разной плотности уровень жидкости в флаконах может различаться',
               'Givaudan x Greenwax',
               'Аромат разработан командой Greenwax совместно с ведущими специалистами крупнейшей парфюмерной корпорации мира',
               'Высочайшие стандарты',
               'Рецептура швейцарской компании соответствует международным стандартам безопасности IFRA и REACH',
               'Экология и безопасность', 'Vegan Friendly', 'Cruelty Free', 'IFRA & REACH', 'Phtalates free',
               'Горячая отдача', 'Ароматы произведены по формуле, разработанной специально для использования в свечах',
               'Многокомпонентность',
               'Синтезированные отдушки с добавлением эфирных масел и душистых веществ органического происхождения']
        for nots in aroma_not:
            arom_not = nots.text
            if arom_not not in list:
                aroma_nots.append(arom_not)
        aroma_nots_list = (f"'Нагрузка для свечей'- {aroma_nots[0]}, Ноты: {aroma_nots[2]} - {aroma_nots[3]}, {aroma_nots[4]} - {aroma_nots[6]}, {aroma_nots[5]} - {aroma_nots[7]} ")
        # выбираем наши нужные данные и создаем файл
        list_aroma.append(
           {
               "Название ароматизатора:": aroma_names1,
               "Описание:": aroma_opisanie.replace('Краткое описание:',''),
               "Примечание:": aroma_nots_list
           }
        )

    # with open ("aroma/aroma_vse.json", 'w', encoding='utf-8') as file: #запись всей информации пр ароматам в файл json
    #     json.dump(list_aroma, file, indent=4, ensure_ascii=False)
    #print(len(list_aroma))

    list_kras = []


    for kras_url in kras_urls:
        req1 = requests.get(kras_url, headers={'User-Agent': UserAgent().chrome})
        kras_name = kras_url.split("/")[-1]
        if kras_name == "":
            kras_name = kras_url.split("/")[-2]
        # with open (f'kras/{kras_name}.html', 'w', encoding='utf-8') as file: #запись страниц с красителем в файлы
        #     file.write(req1.text)

        with open(f'kras/{kras_name}.html', encoding='utf-8') as file:   # открытие страницы с красителем из файла
            src1 = file.read()
            soup1 = bs(src1, "lxml")

        kras_names1 = soup1.find('title').text.replace("Greenwax — Краситель для свечей ", "") #заменяем рекламу на пустой символ, чтобы исключить из названия и оставить краситель
        kras_opisanie = soup1.find('div', class_="t744__descr t-descr t-descr_xxs").text.replace('Представлен в двух вариантах упаковки: в удобной банке для хранения, а также в Zip Lock пакетах для легкого рефила вашей тарыНужен опт? Перейти к оптовым ценам →','.')  # находим данные описания
        kras_rek = soup1.find_all("div", class_="tn-atom")  # находим данные рекомендаций и затем исключаем ненужную информацию, которая в списке list и оставляем только ноты и интенсивность при помощи цикла
        kras_reks = []
        list1 = ['','Примечание: Палитра приведена для примера, конечный цвет зависит от используемого вами воска/парафина, а также точного процента нагрузки','Особенности','Экономичный','Яркие и насыщенные оттенки достигаются при небольшой нагрузке','Комбинирование', 'Удобно смешивать с красителями другими цветов для создания новых вариантов цвета', 'Широкая палитра', 'Разнообразие оттенков достигается изменением нагрузки от 0,05 до 0,5%','Eco-friendly', 'Красители не тестировались на животных и обладают статусами Vegan Friendly и Cruelty Free','В сухом виде в форме хлопьев и гранул, удобных для более точной дозировки', 'Форма','Нагрузка','1','2','3','4']
        for reks in kras_rek:
            kras_rek = reks.text
            if kras_rek not in list1:
                kras_reks.append(kras_rek)


        kras_reks_list = (f"Возможные цвета- {kras_reks[0:5]}, {kras_reks[5]}:  {kras_reks[6]} - {kras_reks[7]}, {kras_reks[8]} - {kras_reks[9]}, {kras_reks[10]} - {kras_reks[11]}, {kras_reks[12]}. ")


        list_kras.append(
            {
           "Название красителя:": kras_names1,
           "Описание:": kras_opisanie.replace('Краткое описание:',''),
           "Примечание:": kras_reks_list
            }
        )
    #print(list_kras)
    # with open("kras/kras_vse.json", 'w', encoding='utf-8') as file:  # запись всей информации пр ароматам в файл json
    #     json.dump(list_kras, file, indent=4, ensure_ascii=False)


parser_aroma("https://greenwax.ru/")