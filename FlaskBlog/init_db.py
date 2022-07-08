import sqlite3

connection = sqlite3.connect('site.db')


with open('schema1.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()