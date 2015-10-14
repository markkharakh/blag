import sqlite3,hashlib

def writePost(title,txt,idu):
    conn = sqlite.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT max(posts.id) FROM posts'
    idp = cur.execute(q).fetchone()[0]
    writePost(title, txt, idp, idu)
    return idp

def writePost(title, txt, idp, idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "INSERT INTO posts(title,content,pid,uid) VALUES(?,?,?,?)"
    conn.execute(q,(title,txt,idp,idu))
    conn.commit()

#writePost("title1","hello",1,1)
#writePost("title2","im sandy",2,1)
#writePost("title3","call me white fang",3,1)
#writePost("title4","im also white bread",4,1)
#writePost("title5","im the leader fear me",5,4)

def getPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.pid = %d"
    result = cur.execute(q%idp).fetchone()
    return result

def getPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %d"
    result = conn.execute(q%idu)
    for r in result:
        print r
    conn.commit()
    return result

def getComments(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * from comments WHERE comments.pid = %d"
    result = conn.execute(q%idp).fetchall()
    return result

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

def getUserId(name):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.id FROM users WHERE users.name = %s'
    result = conn.execute(q%name).fetchone()
    print result
    return result[0]

def addUser(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.name = %s'
    result = conn.execute(q%username)
    print len(result)
    if len(result) == 0:
        q = 'SELECT max(users.id) FROM users'
        uid = cur.execute(q).fetchone()[0]
        q = 'INSERT INTO users VALUES (?, ?, ?)'
        conn.execute(q, (username, encrypt(password), uid+1))
        return True
    return False

print "hello"
print getPost(1)
#print getPost(2)
#print getPost(3)
#print getPost(4)


