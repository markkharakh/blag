import sqlite3,hashlib

def writePost(txt, idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(pid) FROM posts"
    last = conn.execute(q)
    for i in last:
        idp = i[0]+1
    print idp
    q = "INSERT INTO posts(content,pid,uid) VALUES(?,?,?)"
    conn.execute(q,(txt,idp,idu))
    conn.commit()

#writePost("im sandy",2,1)
#writePost("call me white fang",3,1)
#writePost("im also white bread",4,1)
#writePost("im the leader fear me",5,4)
#writePost("i joined track to run away from my problems",3)

def getPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %s"
    result = conn.execute(q%idu)
    for r in result:
        print r
    conn.commit()

def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()
    
def authenticate(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = %s'
    result = conn.execute(q%username)
    for r in result:
        if(encrypt(password) == r[0]):
            return True
    return False

def addUser(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.name = %s'
    result = conn.execute(q%username)
    print len(result)
    if len(result) == 0:
        q = 'SELECT max(users.id) FROM users'
        uid = conn.execute(q)
        q = 'INSERT INTO users VALUES (?, ?, ?)'
        conn.execute(q, (username, encrypt(password), uid+1))
        return True
    return False
    
getPosts(1)
getPosts(2)
getPosts(3)
getPosts(4)


