import sqlite3,hashlib
from pymongo import MongoClient

#Liam is pulling this

# All methods should be rewritten using mongo instead of SQLite

#----------------------------------Writing--------------------------------

def writePost(title, txt, idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(pid) FROM posts"
    idp = cur.execute(q).fetchone()[0]
    if idp == None:
        idp = 0
    print idp+1
    q = "INSERT INTO posts(title,content,uid,pid) VALUES(?,?,?,?)"
    cur.execute(q,(title,txt,idu,idp+1))
    conn.commit()
    return idp + 1

def writeComment(txt, idu, idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT MAX(cid) FROM comments"
    idc = cur.execute(q).fetchone()[0]
    if idc == None:
        idc = 0
    #print idc+1
    q = "INSERT INTO comments(content,cid,pid,uid) VALUES(?,?,?,?)"
    cur.execute(q,(txt,idc+1,idp,idu))
    conn.commit()

def writeProfile(idu, filename, age, color):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "UPDATE users SET age = ?, color = ?, filename = ? WHERE id = ?"
    cur.execute(q,(age,color,filename,idu))
    '''q = "SELECT picid from users where id = %d"
    idpic = cur.execute(q%idu).fetchone()[0]
    print idpic
    q = "UPDATE pics SET filename = ? WHERE id = ?"
    cur.execute(q,(filename,idpic))'''
    conn.commit()
    
#----------------------------------Deleting-------------------------------

def deleteComment(idc):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    deleteCommentH(idc)
    q = "UPDATE comments SET cid = cid-1 WHERE cid > %d"
    cur.execute(q%idc)    
    conn.commit()

def deleteCommentH(idc):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "DELETE FROM comments WHERE comments.cid = %d"
    cur.execute(q%idc)
    conn.commit()

def deletePost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT comments.cid FROM comments WHERE comments.pid = %d"
    bad = cur.execute(q%idp).fetchall()
    for comment in bad:
        deleteCommentH(comment[0])
    q = "UPDATE comments SET cid = rowid"
    cur.execute(q)
    q = "DELETE FROM posts WHERE posts.pid = %d"
    cur.execute(q%idp)
    q = "UPDATE posts SET pid = pid-1 WHERE pid > %d"
    cur.execute(q%idp)    
    conn.commit()

#----------------------------------Getting--------------------------------

def getCommentsOnPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT comments.content,datetime(comments.time,'localtime'),users.name,comments.cid,users.filename FROM comments, users WHERE comments.pid = %d AND users.id = comments.uid"
    result = cur.execute(q%idp).fetchall()
    conn.commit()
    return result

def getComment(cid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT comments.*,users.name FROM comments, users WHERE comments.cid = %d AND users.id = comments.uid"
    result = cur.execute(q%cid).fetchone()
    return result

def getUserPosts(idu):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT * FROM posts WHERE posts.uid = %d"
    result = cur.execute(q%idu).fetchall()
    conn.commit()
    return result

def getPost(idp):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT posts.*,users.name,users.filename FROM posts,users WHERE posts.pid = %d AND posts.uid = users.id"
    result = cur.execute(q%idp).fetchone()
    conn.commit()
    return result

def getAllPosts():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT posts.content,posts.pid,posts.uid,users.name,posts.title,datetime(posts.time,'localtime'),users.filename FROM posts, users WHERE users.id = posts.uid ORDER BY posts.pid DESC"
    cur.execute(q)
    all_rows = cur.fetchall()
    print all_rows
    conn.commit()
    return all_rows

def getAllUsers():
    connection = MongoClient()
    db = connection['data']
    print db.collection_names()
    res = db.users.find()
    all_rows = []
    for i in res:
        all_rows.append(i)
    return all_rows
    """
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = "SELECT users.name FROM users"
    cur.execute(q)
    all_rows = cur.fetchall()
    #print all_rows
    conn.commit()
    return all_rows
    """

def getProfile(uid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT name,filename,age,color FROM users WHERE users.id = %d'
    cur.execute(q%uid)
    row = cur.fetchone()
    conn.commit()
    return row

#----------------------------------Log In---------------------------------
    
def encrypt(word):
    hashp = hashlib.md5()
    hashp.update(word)
    return hashp.hexdigest()

def authenticate(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.password FROM users WHERE users.name = "%s"'
    result = cur.execute(q%username)
    for r in result:
        if(encrypt(password) == r[0]):
            return True
    conn.commit()
    return False

def getUserId(name):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.id FROM users WHERE users.name = "%s"'
    result = cur.execute(q%name).fetchone()
    conn.commit()
    if result==None:
        return None
    return result[0]

def getUserName(uid):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.id = %d'
    result = cur.execute(q%uid).fetchone()
    conn.commit()
    return result[0]

def addUser(username,password):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    q = 'SELECT users.name FROM users WHERE users.name = ?'
    result = cur.execute(q,(username,)).fetchone()
    if result == None:
        q = 'SELECT max(users.id) FROM users'
        uid = cur.execute(q).fetchone()[0]
        if uid==None:
            uid=0
        q = 'INSERT INTO users VALUES (?, ?, ?,-1,-1,"","")'
        cur.execute(q, (username, encrypt(password), uid+1))
        #print str(uid+1)+","+username
        conn.commit()
        return True
    conn.commit()
    return False
