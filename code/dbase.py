import sqlite3
from datetime import date,timedelta
def fun(b,c):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    if b==0 and c==0:
        cursor.execute("SELECT * FROM section")
    elif b==0 and len(c)==2:
        t=f"SELECT * FROM section WHERE {c[1]} = ? "
        values=(c[0],)
        cursor.execute(t,values)
    elif c==0:
        t=f"SELECT ID FROM section WHERE Name='{b}'"
        cursor.execute(t)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def fun2(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    if b==0:
        t=f"SELECT Name,Date,Description FROM section WHERE ID={a}"
    else:
        t=f"SELECT Name,Author,Content,price FROM book WHERE ID={a}"
    cursor.execute(t)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k[0]
def fun1(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    if b==0:
        txt=f"SELECT X.* FROM book X WHERE X.SectionID={a} "
        cursor.execute(txt)
        k=cursor.fetchall()
    else:
        t=f"SELECT X.* FROM book X WHERE X.{b[1]}= ? AND X.SectionID={a}"
        values=(b[0],)
        cursor.execute(t,values)
        k=cursor.fetchall()
    txt=f"SELECT Name FROM section WHERE ID={a}"
    cursor.execute(txt)
    b=cursor.fetchall()
    conn.commit()
    conn.close()
    return (k,b[0][0])
def addsection(a1,a2,a3):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(ID) FROM section")
    k=cursor.fetchall()[0][0]
    txt = "INSERT INTO section VALUES (?, ?, ?, ?)"
    values = (k+1, a1, a2, a3)
    cursor.execute(txt, values)
    conn.commit()
    conn.close()
def addbook(a1,a2,a3,a4,a5):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT MAX(X.ID),Y.ID FROM book X JOIN section Y ON X.SectionID = Y.ID  WHERE Y.Name='{a4}'"
    cursor.execute(t)
    k=cursor.fetchall()[0]
    txt = "INSERT INTO book VALUES (?, ?, ?, ?, ?, ?, ?)"
    if k[0]!=None:
        values = (k[0]+1, a1, a2, a3,k[1],a5,0)
    else:
        a=fun(a4,0)[0][0]
        values = (a*100, a1, a2, a3,a,a5,0)
    cursor.execute(txt, values)
    conn.commit()
    conn.close()
def adduser(a1,a2,a3,a4,a5,a6):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    txt = "INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)"
    values = (a1, a2, a3, a4, a5, a6)
    cursor.execute(txt, values)
    conn.commit()
    conn.close()   
def userchk(un,pwd):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    txt=f"SELECT * FROM user WHERE uname='{un}' AND Pwd='{pwd}'"
    cursor.execute(txt)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def dummy(e):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT X.Name,X.Author,Y.Name,X.ID,X.price,X.rating FROM book X JOIN section Y ON X.SectionID = Y.ID WHERE {e}"
    cursor.execute(t)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def search(a,b,c):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t1=f"SELECT bookid FROM main WHERE username='{c}' AND status IN ('granted','completed','request')"
    cursor.execute(t1)
    t1=cursor.fetchall()
    l=(0,)
    if t1!=[]:
        for i in t1:
            l+=(i[0],)
    else:
        l=()
    if b=="Section":
        s=f"Y.Name='{a}' AND X.ID NOT IN {l}"
        k=dummy(s)
        return k
    elif b=="Author":
        s=f"X.Author='{a}' AND X.ID NOT IN {l}"
        k=dummy(s)
        return k
    else:
        s=f"X.Name='{a}' AND X.ID NOT IN {l}"
        k=dummy(s)
        return k
    conn.commit()
    conn.close()
def userdash(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t1=f"SELECT bookid FROM main WHERE username='{a}' AND status IN ('request','granted','completed')"
    cursor.execute(t1)
    t1=cursor.fetchall()
    l=(0,)
    if t1!=[]:
        for i in t1:
            l+=(i[0],)
    else:
        l=()
    t=f"SELECT X.Name,X.Author,Y.Name,X.ID,X.price,X.rating FROM book X JOIN section Y ON X.SectionID = Y.ID WHERE X.ID NOT IN {l} ORDER BY X.rating DESC"
    cursor.execute(t)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def req(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT SectionID,ID FROM book WHERE ID={a}"
    cursor.execute(t)
    k=cursor.fetchall()
    txt = "INSERT INTO main VALUES (?, ?, ?, ?, ?, ?)"
    values =k[0]+(b,date.today(),'0-0-0','request')
    cursor.execute(txt, values)
    conn.commit()
    conn.close()
def libchoice(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    query = "UPDATE main SET status='granted', Return_date=? WHERE bookid=? AND username=?"
    values = (str(date.today() + timedelta(days=7)), a, b)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
def default():
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"UPDATE main SET status='completed' WHERE Return_date='{date.today()}' "
    cursor.execute(t)
    conn.commit()
    conn.close()
def revoke(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"UPDATE main SET status='completed' WHERE bookid={a} and username='{b}'"
    cursor.execute(t)
    conn.commit()
    conn.close()
def userreq(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t='''SELECT X.Name,X.Author,Y.Name,X.id,X.price,X.rating,X.Content FROM book X JOIN section Y ON X.SectionID = Y.ID
    WHERE (X.SectionID,X.ID) IN (SELECT sectionid,bookid FROM main WHERE username= ? and status= ?) '''
    cursor.execute(t,(a,b))
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def libreq(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t='''SELECT z.uname, X.Name, A.Name, X.ID FROM book X
    JOIN main Y ON X.ID = Y.bookid JOIN user z ON Y.username = z.uname JOIN section A ON A.ID = X.SectionID WHERE Y.status = ?'''
    cursor.execute(t,(a,))
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k

def reject(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"DELETE FROM main WHERE bookid={a} and username='{b}'"
    cursor.execute(t)
    conn.commit()
    conn.close()
def delesec(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT Content FROM book WHERE SectionID={a}"
    cursor.execute(t)
    k=cursor.fetchall()
    t=f"DELETE FROM section WHERE ID={a}"
    cursor.execute(t)
    t=f"DELETE FROM book WHERE SectionID={a}"
    cursor.execute(t)
    conn.commit()
    conn.close()
    return k
def delebook(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT Content FROM book WHERE ID={a}"
    cursor.execute(t)
    k=cursor.fetchall()
    t=f"DELETE FROM book WHERE ID={a}"
    cursor.execute(t)
    conn.commit()
    conn.close()
    return k
def update(a1,a2,a3,a4,b,c,a5):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    if b==0:
        t=f"UPDATE section SET Name='{a1}',Date='{a2}',Description='{a3}' WHERE ID={a4}"
    else:
        txt=f"SELECT ID FROM section WHERE Name='{a4}'"
        cursor.execute(txt)
        d=cursor.fetchall()
        t=f"UPDATE book SET Name='{a1}',Author='{a2}',Content='{a3}',price={a5} WHERE SectionID={d[0][0]} AND ID={c}"
        print(t)
    cursor.execute(t)
    conn.commit()
    conn.close()
def userdetail(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT * FROM user WHERE uname='{a}'"
    cursor.execute(t)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k[0]
def deluser(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"DELETE FROM user WHERE uname='{a}'"
    cursor.execute(t)
    conn.commit()
    conn.close()
def bookdet(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t = f"SELECT X.email, X.number, COUNT(CASE WHEN Y.status = 'granted' THEN 1 ELSE NULL END) FROM user X JOIN main Y ON X.uname = Y.username WHERE X.uname = ?  GROUP BY X.email, X.number"
    cursor.execute(t, (a,))
    k = cursor.fetchall()
    t = f"SELECT x.bookid,x.Return_date,y.Name FROM main x join book y on x.bookid=y.ID WHERE x.username = ? AND x.status = 'granted' "
    cursor.execute(t, (a,))
    k1= cursor.fetchall()
    conn.commit()
    conn.close()
    return k[0],k1
def uprate(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT rating FROM book WHERE Name='{a}'"
    cursor.execute(t)
    k=cursor.fetchall()
    if int(b)>k[0][0]:
        t=f"UPDATE book SET rating={b} WHERE Name='{a}'"
        cursor.execute(t)
    conn.commit()
    conn.close()
def bookstat(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT Name,price,rating,SectionID FROM book WHERE ID='{a}'"
    cursor.execute(t)
    k=cursor.fetchall()
    t=f"SELECT username,Return_date FROM main WHERE bookid='{a}' AND status='granted'"
    t1=f"SELECT username FROM main WHERE bookid='{a}' AND status='completed'"
    t2=f"SELECT username FROM main WHERE bookid='{a}' AND status='request'"
    cursor.execute(t)
    k1=cursor.fetchall()
    cursor.execute(t1)
    k2=cursor.fetchall()
    cursor.execute(t2)
    k3=cursor.fetchall()
    conn.commit()
    conn.close()
    return k[0],k1,k2,k3
def chk(a):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t=f"SELECT COUNT(*) FROM main WHERE username='{a}' AND status='request' GROUP BY username"
    cursor.execute(t)
    k=cursor.fetchall()
    print(k)
    conn.commit()
    conn.close()
    if k==[]:
        return True
    if k[0][0]<5 :
        return True
    else:
        return False
