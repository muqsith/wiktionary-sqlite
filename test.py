#!/usr/bin/env python3.5
import sqlite3
import zlib

def test_data():
    conn = sqlite3.connect('enwiktionary.db')
    c = conn.cursor()
    query = ''' SELECT * FROM enwiktionary where title like '%apple%' '''
    c.execute(query)
    l = c.fetchall()
    print(len(l))
    for t in l:
        text = zlib.decompress(t[1])
        print(str(text))

def test_title():
    conn = sqlite3.connect('enwiktionary.db')
    c = conn.cursor()
    query = ''' select title, count(title) as title_count
        from enwiktionary group by title having title_count > 1'''
    c.execute(query)
    l = c.fetchall()
    print(len(l), '- Records')
    print('Title, ', 'Count', '\n')
    for t in l:
        print(t[0], t[1], '\n')

if __name__ == "__main__":
    test_data()
