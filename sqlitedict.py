import sqlite3
conn = sqlite3.connect('enwiktionary.db')
c = conn.cursor()

def create_db():
    try:
        c.execute('''CREATE TABLE enwiktionary
             (title text primary key, data text, weight int, char_sort text)''')
    except Exception as err:
        print('Error occured while creating table \n', err)

def insert_values(t):
    try:
        c.execute("INSERT INTO enwiktionary VALUES (?, ?, ?, ?)", t)
    except Exception as err:
        print('Error occured while insertion of record \n')
        print('title: ', t[0], '\t')
        print('weight: ', t[2], '\t')
        print('char_sort: ', t[3], '\t')
        print(err)

def create_index():
    try:
        c.execute(''' CREATE UNIQUE INDEX alpha on enwiktionary (title) ''')
    except Exception as err:
        print('Error occured while creating index on table \n', err)

def commit():
    try:
        conn.commit()
    except Exception as err:
        print('Error occured while committing records to db \n', err)

def close_db():
    try:
        conn.close()
    except Exception as err:
        print('Error occured while closing db connection \n', err)
