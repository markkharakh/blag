import sqlite3,hashlib

def writePost(txt, idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(pid) FROM posts"
    last = cur.execute(q)
    idp = 1
    for i in last:
        if i[0]!=None:
            idp = i[0]+1
    print idp
    q = "INSERT INTO posts(content,pid,uid) VALUES(?,?,?)"
    cur.execute(q,(txt,idp,idu))
    conn.commit()

def writeComment(txt, idu, idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(cid) FROM comments"
    last = cur.execute(q)
    idc = 1
    for i in last:
        if i[0]!=None:
            idc = i[0]+1
    print idc
    q = "INSERT INTO comments(content,cid,pid,uid) VALUES(?,?,?,?)"
    cur.execute(q,(txt,idc,idp,idu))
    conn.commit()

def getPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.pid = %d"
    result = cur.execute(q%idp).fetchone()
    return result

def getCommentsOnPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM comments WHERE comments.pid = %s"
    result = cur.execute(q%idp)
    comments = []
    for r in result:
        comments.append(r)
    conn.commit()
    return comments

def getUserPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %s"
    result = cur.execute(q%idu)
    posts = []
    for r in result:
        posts.append(r)
    conn.commit()
    return posts

def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()
    
def authenticate(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = %s'
    result = cur.execute(q%username)
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
    result = cur.execute(q%username)
    print len(result)
    if len(result) == 0:
        q = 'SELECT max(users.id) FROM users'
        uid = cur.execute(q).fetchone()[0]
        q = 'INSERT INTO users VALUES (?, ?, ?)'
        cur.execute(q, (username, encrypt(password), uid+1))
        return True
    return False

#writePost("im sandy",2,1)
#writePost("call me white fang",3,1)
#writePost("im also white bread",4,1)
#writePost("im the leader fear me",5,4)
#writePost("i joined track to run away from my problems",3)
#writePost("kms",2)

#writeComment("lol i hate u",1,7)
#writeComment("who do u think u r",3,7)
#writeComment("gr8 work snad",1,4)
    
print getUserPosts(1)
print getUserPosts(2)
print getUserPosts(3)
print getUserPosts(4)

print getCommentsOnPost(4)
print getCommentsOnPost(6)
print getCommentsOnPost(7)
