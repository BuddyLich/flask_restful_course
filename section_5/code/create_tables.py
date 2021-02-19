import sqlite3

connection = sqlite3.connect('../data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
# real: a number with a decimal point

connection.commit()
connection.close()
