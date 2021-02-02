import sqlite3


def create_db():
    #Создаем базу ссылок сайта
    db = sqlite3.connect('all_url.db')
    cur = db.cursor() 
    #Добавляем в БД столбцы
    cur.execute("""
                CREATE TABLE IF NOT EXISTS all_url ( 
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Title TEXT,
                    Url TEXT,
                    Count INT
                    )""")


def create_db_follow():
    #Создаем базу переходов
    db_follow = sqlite3.connect('follows_url.db')
    cur_follow = db_follow.cursor() 
    #Добавляем в БД столбцы
    cur_follow.execute("""CREATE TABLE IF NOT EXISTS follows_url ( 
                            № INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            Home_link TEXT,
                            Follow_link TEXT
                        )""")


def add_db(html, title): # добавление ссылки в базу данных
    db = sqlite3.connect('all_url.db')
    cur = db.cursor() 
    print('add db - ' + html)
    cur.execute(f"INSERT INTO all_url (Title, Url, Count) VALUES (?, ?, ?)", (title, html, 1))
    db.commit()


def add_db_follow(html, urls): # добавление ссылки и ее переходов в базу данных
    db_follow = sqlite3.connect('follows_url.db')
    cur_follow = db_follow.cursor() 
    print('add db follow - ' + html)
    cur_follow.execute(f"INSERT INTO follows_url (Home_link, Follow_link) VALUES (?, ?)", (html, urls, ))
    db_follow.commit()


def add_count_in_db(html): # увеличение показателя встречи страницы
    db = sqlite3.connect('all_url.db')
    cur = db.cursor() 
    print('count ' + html)
    cur.execute(f"UPDATE all_url SET Count = Count+1 WHERE Url LIKE ?", (html,))
    db.commit()


