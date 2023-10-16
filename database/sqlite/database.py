'''
This code is good for creating a database from a json file. If you want to create a database from a json file, you can use this code. But this code takes up a lot of memory and time,
and it's not very efficient for me, at least not in the way I'm thinking right now. I'm going to keep this code, but for updated code, check the dask folder in this project.
'''

import sqlite3
import json
from datetime import datetime
import multiprocessing

timeframe = '2015-01'
sql_transaction = []
file_path = "database/RC_2015-01"
db_lock = multiprocessing.Lock()

# Connect to database (creates a new database if it doesn't exist)

def get_connection():
    conn = sqlite3.connect('reddit_data.db')
    c = conn.cursor()
    return (conn, c)

def create_table(): 
    try:
        db_lock.acquire()
        conn, c = get_connection()
        c.execute("""CREATE TABLE IF NOT EXISTS parent_reply
                (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT,
                comment TEXT, subreddit TEXT, unix INT, score INT)""")
        conn.close()
    finally:
        db_lock.release()


def format_data(data):
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")
    return data


def find_parent(pid):
    try:
        db_lock.acquire()
        conn, c = get_connection()
        sql = "SELECT comment FROM parent_reply WHERE comment_id like '%{}%' LIMIT 1".format(pid.split('_')[1])
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
        conn.close()
    except Exception as e:
        print("find_parent", e)
        return False
    finally:
        db_lock.release()
    
def find_existing_score(pid):
    try:
        db_lock.acquire()
        conn, c = get_connection()
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
        conn.close()
    except Exception as e:
        print("find_existing_score", e)
        return False
    finally:
        db_lock.release()
    
def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True
    
def transaction_bldr(sql):
    try:
        db_lock.acquire()
        conn, c = get_connection()
        c.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print("transaction_bldr", e)
    finally:
        db_lock.release()
    
def sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ?
                WHERE parent_id = ?""".format(parent_id, comment_id, parent_data, body, subreddit, int(created_utc), score, parent_id)
        transaction_bldr(sql)
    except Exception as e:
        print("sql_insert_replace_comment", e)

def sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score)
                VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")""".format(parent_id, comment_id, parent_data, body, subreddit, int(created_utc), score)
        transaction_bldr(sql)
    except Exception as e:
        print("sql_insert_has_parent", e)

def sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score)
                VALUES ("{}", "{}", "{}", "{}", "{}", "{}")""".format(parent_id, comment_id, body, subreddit, int(created_utc), score)
        transaction_bldr(sql)
    except Exception as e:
        print("sql_insert_no_parent", e)

if __name__=="__main__":
    create_table()
    row_counter = 0
    paired_rows = 0
    
    with open(file_path, buffering=1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            comment_id = row['id']
            parent_data = find_parent(parent_id)

            #search for comments with a score of 2 or more
            if score >= 2:
                if acceptable(body):
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                    else:
                        if parent_data:
                            sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                            paired_rows += 1
                        else:
                            sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)

            if row_counter % 100000 == 0:
                print("Total rows read: {}, Paired rows: {}, Time: {}".format(row_counter, paired_rows, str(datetime.now())))