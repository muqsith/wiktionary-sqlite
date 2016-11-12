import sqlite3
conn = sqlite3.connect('enwiktionary.db')
c = conn.cursor()

def create_db():
    try:
        c.execute('''CREATE TABLE enwiktionary
             (checksum text, title text, data text, weight int, char_sort text)''')
    except Exception as err:
        print(err)

def insert_values(t):
    try:
        c.execute("INSERT INTO enwiktionary VALUES (?, ?, ?, ?, ?)", t)
    except Exception as err:
        print(err)

def close_db():
    conn.commit()
    conn.close()
