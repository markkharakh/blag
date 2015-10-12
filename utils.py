import sqlite3

def writePost(txt, idp, idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "INSERT INTO posts(content,pid,uid) VALUES(?,?,?)"
    conn.execute(q,(txt,idp,idu))
    conn.commit()

#writePost("im sandy",2,1)
#writePost("call me white fang",3,1)
#writePost("im also white bread",4,1)
#writePost("im the leader fear me",5,4)

def getPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %s"
    result = conn.execute(q%idu)
    for r in result:
        print r
    conn.commit()

getPosts(1)
getPosts(2)
getPosts(3)
getPosts(4)


