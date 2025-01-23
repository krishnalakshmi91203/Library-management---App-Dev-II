import os
from twilio.rest import Client
import sqlite3
from datetime import datetime
import csv
def fetch_ebook_data():
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t='''SELECT X.Name,X.Content,X.Author,Y.username,Y.Date_issued,Y.Return_date,Y.status FROM book X
    JOIN main Y ON X.ID = Y.bookid '''
    cursor.execute(t)
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def export_ebook_data():
    data = fetch_ebook_data() 
    print(data) 
    csv_file_path = "static/exported_ebooks.csv"
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Book Name", "Content", "Author(s)","User Name" "Date Issued", "Return Date", "Status"])
        for book in data:
            writer.writerow([book[0], book[1], book[2], book[3], book[4], book[5],book[6]])
    return csv_file_path

def date_time(a):
    date_format = "%Y-%m-%d"
    date1 = datetime.strptime(a, date_format)
    today = datetime.today()
    date_diff = (today - date1).days
    return date_diff
def detail(a,b):
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t='''SELECT z.uname,z.Name,z.number,X.Name FROM book X
    JOIN main Y ON X.ID = Y.bookid JOIN user z ON Y.username = z.uname 
    WHERE Y.bookid = ? AND z.uname= ? AND y.status=? '''
    cursor.execute(t,(a,b,"granted"))
    k=cursor.fetchall()
    conn.commit()
    conn.close()
    return k
def reminder():
    account_sid = 'AC5245f506198b6fd1ec12a9c44fc655bf'#os.environ["TWILIO_ACCOUNT_SID"]
    auth_token ='dbce11d365fe4b5ab3447f4c50fdc080'#os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    cursor.execute("SELECT bookid,username,Return_date FROM main where status='granted'")
    k=cursor.fetchall()
    print(".............sms sent to:..............\n",k)
    for i in k:
        b=date_time(i[2])
        if b in {2, 1, 0}:
            d=detail(i[0],i[1])
            c=f"""
            \n Hi {d[0][0]},\n\nYour book "{d[0][3]}" is due for return on {i[2]}. Only {b} day(s) left! Please return it on time.\n\nThank you,\nKL Library"""
            e=f"+91{d[0][2]}"
            message = client.messages.create(
            body=c,
            from_="+12513561445",
            to=e,)
            print(message.body)

#......................mail.......................
def fetch():
    conn = sqlite3.connect('merge.db')
    cursor = conn.cursor()
    t='''SELECT username, Date_issued, Return_date, status 
FROM main WHERE (Date_issued >= date('now', 'start of month', '-1 month') 
    AND Date_issued < date('now', 'start of month'))
  OR (Return_date >= date('now', 'start of month', '-1 month') 
    AND Return_date < date('now', 'start of month'));
'''
    cursor.execute(t)
    k=cursor.fetchall()
    t="SELECT X.Name,Y.Name,X.rating FROM book X JOIN section Y ON X.SectionID = Y.ID "
    cursor.execute(t)
    k1=cursor.fetchall()
    conn.commit()
    conn.close()
    return k,k1

REPORT_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <title>Monthly Activity Report</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Monthly Activity Report</h1>
    
    <h2>Issued E-Books</h2>
    <table>
        <thead>
            <tr>
                <th>Username</th>
                <th>Issued Date</th>
                <th>Return Date</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
        {% for entry in issued_books %}
            <tr>
                <td>{{ entry[0] }}</td>
                <td>{{ entry[1] }}</td>
                <td>{{ entry[2] }}</td>
                <td>{{ entry[3] }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    
    <h2>Book Ratings</h2>
    <table>
        <thead>
            <tr>
                <th>Title</th>
                <th>Genre</th>
                <th>Rating</th>
            </tr>
        </thead>
        <tbody>
        {% for book in book_ratings %}
            <tr>
                <td>{{ book[0] }}</td>
                <td>{{ book[1] }}</td>
                <td>{{ book[2] }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''