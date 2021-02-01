import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3

url_from_page_start = []
urls_met = []
stack = []
url = 'https://quotes.toscrape.com/'
host = 'https://quotes.toscrape.com'
#получение доступа к странице
# page = requests.get(url) 
# print(page.status_code) #проверка статуса страницы

# print(title)

#Создаем базу
db = sqlite3.connect('all_url.db')
#Добавляем в БД столбцы
cur = db.cursor() 
cur.execute("""
             CREATE TABLE IF NOT EXISTS all_url ( 
                 Title TEXT,
                 Url TEXT,
                 Count INT
                 )""")
db.commit()


def add_db(html): # добавление ссылки в базу данных
    print('add db - ' + html)
    title = get_title(html)
    cur.execute(f"INSERT INTO all_url VALUES (?, ?, ?)", (title, html, 1))
    db.commit()


def add_count_in_db(html): # увеличение показателя ее встречи
    print('count ' + html)
    cur.execute(f"UPDATE all_url SET Count = Count+1 WHERE Url LIKE ?", (html,))
    db.commit()


def get_page(html):# получение страницы
    page = requests.get(html)
    return page


def get_title(html): # получение заголовка страницы
    page = requests.get(html)
    if page.status_code == 200:
        #получение страницы в объекты супа
        soup = BeautifulSoup(page.text, 'html.parser')
        # поиск заголовка страницы
        title=soup.title.text 
        return title
    else:
        print('Error')


def get_content(html): #получает url со страницы и проверяет их правильность
    url = []
    page = get_page(html)
    if page.status_code == 200:
        #получение страницы в объекты супа
        soup = BeautifulSoup(page.text, 'html.parser')
        #поиск всех атрибутов href во всех тегах а
        #и проверка на относительные ссылки
        for a in (tag['href'] for tag in soup('a')):
            if not a.startswith('http'):
                a = urljoin(host, a)
            url.append(a)
        return url
    else:
        print('Error')


def check_in_or_out_url(html): #проверка ссылок на внешние и внутренние
    print('check ' + html)
    if html.startswith(host):
        print("in url - " + html)
        return html
    else:
        print("out url - " + html)
        return False


count = 0
url_from_page_start = get_content(url)
print(len(url_from_page_start))
for i in url_from_page_start:
    if i not in stack:
        add_db(i)
    else:
        add_count_in_db(i)
    urls_met.append(i)
    stack.append(i)
print('stack - ' + str(len(stack)))
while stack != []:
    print('len stack = ' + str(len(stack)))
    url_from_stack = stack.pop()
    while check_in_or_out_url(url_from_stack) == False:
        add_count_in_db(url_from_stack)
        url_from_stack = stack.pop()
    else:
        new_urls = get_content(url_from_stack)
        print('new_urls - ' + str(len(new_urls)))
        for i in new_urls:
                if i not in urls_met:
                    add_db(i)
                    stack.append(i)
                    urls_met.append(i)
                else:
                    add_count_in_db(i)
else:
    print('end')
