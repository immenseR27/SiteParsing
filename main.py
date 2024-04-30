"""Ecology site parsing program"""
import os
import requests
from bs4 import BeautifulSoup
import pandas
result_list = {'Ссылка': [], 'Дата': [], 'Заголовок': [], 'Текст': []}
FILE_NAME = "parsed_page.csv"
URL = "https://www.vedomosti.ru/ecology"
TIME = 5
r = requests.get(URL, timeout=TIME)
soup = BeautifulSoup(r.content, 'html.parser')
issues = soup.find_all('a', class_='release__link')
for issue in issues:
    URL2 = os.path.split(URL)[0] + issue.get('href', timeout=TIME)
    r = requests.get(URL2, timeout=TIME)
    soup = BeautifulSoup(r.content, 'html.parser')
    main_new = soup.find('a', class_='card-background articles-cards-list__card '
                                     'cols-2 rows-3 --background')
    news = soup.find_all('a', class_='articles-cards-list__card card-article '
                                     'cols-1 rows-3 --article')
    news.insert(0, main_new)
    date = soup.find('time', class_='card-article__date')
    for new in news:
        result_list['Дата'].append(date.get_text())
        URL3 = os.path.split(URL)[0] + new.get('href', timeout=TIME)
        result_list['Ссылка'].append(URL3)
        r = requests.get(URL3, timeout=TIME)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('h1', class_='article-headline__title').get_text().replace('\n', '')
        result_list['Заголовок'].append(title)
        ps = soup.find_all('p', class_='box-paragraph__text')
        text = soup.find('em', class_='article-headline__subtitle').get_text()
        for p in ps:
            text = text + (p.get_text())
        result_list['Текст'].append(text)
data_frame = pandas.DataFrame(result_list)
data_frame.to_csv(FILE_NAME)
