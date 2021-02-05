import requests
import sqlite3
import pytest

@pytest.fixture
def setup_db():
    conn = sqlite3.connect('all_url.db')
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS all_url ( 
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Title TEXT,
                    Url TEXT,
                    Count INT
                    )""")
    sample_data = [
        ('Title_1', 'Url_1', 1),
        ('Title_2', 'Url_2', 1),
    ]
    cursor.executemany('INSERT INTO all_url (Title, Url, Count) VALUES(?, ?, ?)', sample_data)
    yield conn


def test_connection(setup_db):
    # Test to make sure that there are 2 items in the database

    cursor = setup_db
    assert len(list(cursor.execute('SELECT * FROM all_url'))) == 2


