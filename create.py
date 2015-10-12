import sqlite3

conn = sqlite3.connect("data.db")

c = conn.cursor()

q = "create table users(name text, password text, id integer)"
c.execute(q)

q = "create table posts(content text, pid integer, uid integer)"
c.execute(q)

q = "create table comments(content text, cid integer, pid integer, uid integer)"
c.execute(q)

#q = "create table relations(uid integer, pid integer, cid integer)"
#c.execute(q)

conn.commit()

