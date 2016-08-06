import sys
import sqlite3

conn = sqlite3.connect('colorizebot.db')
cursor = conn.cursor()
try:
    cursor.execute("CREATE TABLE Links_Replied (Id INTEGER PRIMARY KEY AUTOINCREMENT, Link_ID TEXT, Link TEXT,colorized_Link TEXT);")
    cursor.execute("CREATE TABLE Comments_Replied (Id INTEGER PRIMARY KEY AUTOINCREMENT, comment_id TEXT);")

except:
    if conn:
        conn.rollback()
    sys.exit(1)

conn.commit()
