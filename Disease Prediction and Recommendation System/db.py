import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Muskan18!!',
    database= 'dbname'
)

cur = db.cursor()

def exist_mail(m):
    cur.execute("SELECT email from login_details;")
    fall = cur.fetchall()
    for i in fall:
        e = i[0]
        if m.lower() == e.lower():
            return True 
    return False

def insert_data(name,email,pwd):
    query = "INSERT INTO login_details (name, email, psw) VALUES (%s,%s,%s);"
    val = [name,email,pwd]
    cur.execute(query,val)
    db.commit()

def check_mail_pwd(mail,pwd):
    if exist_mail(mail)==True:
        query = "SELECT psw from login_details WHERE email = %s;"
        cur.execute(query,[mail])
        passwd = cur.fetchone()[0]
        if passwd==pwd:
            return True
        else:
            return False
    else:
        return False

def get_info(v):
    query = "SELECT * from login_details WHERE email = %s;"
    cur.execute(query,[v])
    all_data = cur.fetchone()
    return all_data


