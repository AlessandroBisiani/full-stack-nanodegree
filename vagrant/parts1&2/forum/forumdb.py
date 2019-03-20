# "Database code" for the DB Forum.
#!/usr/bin/python

import datetime
import psycopg2


def get_posts():
  db = psycopg2.connect("dbname=news")
  cursor = db.cursor()
  cursor.execute("select * from posts order by time desc;")
  posts = cursor.fetchall()
  db.close()
  return posts

def add_post(content):
  db = psycopg2.connect("dbname=news")
  cursor = db.cursor()
  cursor.execute("insert into posts values('%s');", (content,))
  db.commit()
  db.close()