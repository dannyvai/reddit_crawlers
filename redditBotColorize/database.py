import sqlite3
import secret_keys

conn = sqlite3.connect('colorizebot.db')
cursor = conn.cursor()

def save_database():
    try:
        conn.commit()
    except:
        conn.rollback

def add_thread(key,value,value2):
    cursor.execute('INSERT INTO Links_Replied(Link_ID,Link,colorized_Link) VALUES(?,?,?)',((key,value,value2)))
    save_database()

def add_comment(comment_id):
    print comment_id
    cursor.execute('INSERT INTO Comments_Replied(comment_id) VALUES(?)',(comment_id,))
    save_database()


def did_reply_comment(comment_id):
    t = (comment_id,)
    cursor.execute("SELECT * from Comments_Replied WHERE comment_id like ?", t)
    rows = cursor.fetchall()
    return len(rows) > 0
   

def did_reply_thread(thread_id):
    t = (thread_id,)
    cursor.execute("SELECT * from Links_Replied WHERE Link_ID like ?", t)
    rows = cursor.fetchall()
    return len(rows) > 0
    
