import requests
from bs4 import BeautifulSoup
import sqlite3


#Задаем адрес сайта
URL = 'https://quotes.toscrape.com/' #input('Введите адрес: ')
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'accept': '*/*'}
HOST = 'https://quotes.toscrape.com' #input('Укажите ХОСТ: ')

urls_visited = set()

#Создаем базу
db = sqlite3.connect('all_url.db')
#Добавляем в БД столбцы
cur = db.cursor() 
cur.execute("""
             CREATE TABLE IF NOT EXISTS all_url ( 
                 Title TEXT,
                 Url TEXT,
                 Count INT,
                 UNIQUE(URL)
             )""")
db.commit()
#con.close()

def get_html(url=URL, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html): #получение всех ссылок со страницы
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a')
    url=[]
    for item in items:
        url.append(HOST + item.get('href'))
    return url

def get_title(html): #функция получения заголовка страницы
    title = 'Заголовок 1' #TODO добавление в базу заголовка страницы
    URL = html
    #добавление в БД страницу
    if URL not in urls_visited:
        cur.execute(f"INSERT INTO all_url VALUES (?, ?, ?)", (title, URL, 1))
    else:
        for i in cur.execute(f"SELECT Count FROM all_url WHERE Url = URL"):
            count = i[0]
        cur.execute(f"UPDATE all_url SET Count = {1+count} WHERE Url = URL")
    db.commit()


def parse():
    html = get_html() #получение страницы
    if html.status_code == 200: #проверка доступности страницы
        urls = get_content(html.text)
        for i in urls:
            get_title(i) #получение данных страницы в БД
            urls_visited.add(i)
        else:
            print('Страница спарсена')                          
    else:
        print('Error')

parse()
