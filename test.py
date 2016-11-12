import sqlite3
#conn = sqlite3.connect('en-wiktionary.db')
conn = sqlite3.connect('enwiktionary.db')

c = conn.cursor()
c.execute('SELECT * FROM enwiktionary')
print(c.fetchone())
