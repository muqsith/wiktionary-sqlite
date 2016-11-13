#!/usr/bin/env python3.5
import sqlite3
import zlib

def test_data():
    conn = sqlite3.connect('enwiktionary.db')
    c = conn.cursor()
    query = ''' SELECT * FROM enwiktionary where title like '%opt' '''
    c.execute(query)
    l = c.fetchall()
    print(len(l))
    for t in l:
        text = zlib.decompress(t[2])
        print(str(text))

def test_checksum():
    conn = sqlite3.connect('enwiktionary.db')
    c = conn.cursor()
    query = ''' select checksum, count(checksum) as checksum_count
        from enwiktionary group by checksum having checksum_count > 1'''
    c.execute(query)
    l = c.fetchall()
    print(len(l), '- Records')
    print('Checkusm, ', 'Count', '\n')
    for t in l:
        print(t[0], t[1], '\n')

def test_duplicate_checksum_titles():
    conn = sqlite3.connect('enwiktionary.db')
    c = conn.cursor()
    query = ''' select title, checksum from enwiktionary where checksum in
    (select checksum from enwiktionary
    group by checksum having count(checksum) > 1) order by checksum'''
    c.execute(query)
    l = c.fetchall()
    print(len(l), '- Records')
    print('title, ', 'checksum', '\n')
    for t in l:
        print(t[0], t[1], '\n')

if __name__ == "__main__":
    test_data()
