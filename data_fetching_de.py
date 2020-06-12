#!C:\Python36\python.exe

print("Content-Type: text/HTML")
print()

import pandas as pd

import cgi

form = cgi.FieldStorage()
section = form.getvalue("section")

data = pd.read_html("file:///C:/Users/Nikhil/Downloads/report.html")

def na_fill(args):
    for each in args:
        each.fillna(value=0, inplace=True)
    return args

def sem_data(raw_data):
    a = []
    for i in range(7, len(raw_data), 7):
        a.append(raw_data[i])
    for j in range(10, len(raw_data), 7):
        a.append(raw_data[j])
    return a

def final_sem(raw_sem):
    z = list()

    for j in range(len(raw_sem)):
        if len(a[j]) < 4:
            continue
        if ((raw_sem[j][0][5][3]) == '1' or (raw_sem[j][0][4][3]) == '1'):
            sem1 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '2' or (raw_sem[j][0][4][3]) == '2'):
            sem2 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '3' or (raw_sem[j][0][4][3]) == '3'):
            sem3 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '4' or (raw_sem[j][0][4][3]) == '4'):
            sem4 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '5' or (raw_sem[j][0][4][3]) == '5'):
            sem5 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '6' or (raw_sem[j][0][4][3]) == '6'):
            sem6 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '7' or (raw_sem[j][0][4][3]) == '7'):
            sem7 = (raw_sem[j])
        elif ((raw_sem[j][0][5][3]) == '8' or (raw_sem[j][0][4][3]) == '8'):
            sem8 = (raw_sem[j])
    try:
        if len(sem1) != 1:
            z.append(sem1)
    except:
        pass
    try:
        if len(sem2) != 1:
            z.append(sem2)
    except:
        pass
    try:
        if len(sem3) != 1:
            z.append(sem3)
    except:
        pass
    try:
        if len(sem4) != 1:
            z.append(sem4)
    except:
        pass
    try:
        if len(sem5) != 1:
            z.append(sem5)
    except:
        pass
    try:
        if len(sem6) != 1:
            z.append(sem6)
    except:
        pass
    try:
        if len(sem7) != 1:
            z.append(sem7)
    except:
        pass
    try:
        if len(sem8) != 1:
            z.append(sem8)
    except:
        pass
    return z


def personal_data(arg):
    try:
        course = arg[2][2][1]
    except:
        course = arg[2].iloc[1][2]
    try:
        name = arg[2][2][3]
    except:
        name = arg[2].iloc[3][2]

    try:
        roll_no = arg[2][2][2]
    except:
        roll_no = arg[2].iloc[2][2]

    try:
        branch = arg[2][5][1]
    except:
        branch = arg[2].iloc[1][5]
    try:
        college = arg[2][2][0]
    except:
        college = arg[2].iloc[0][2]

    try:
        gender = arg[2][5][4]
    except:
        gender = arg[2].iloc[4][5]
    return roll_no, name, branch, gender, course, college


a = na_fill(sem_data(data))
b = final_sem(a)

roll_no,name,branch,gender,course,college=personal_data(data)

import mysql.connector

con = mysql.connector.connect(user='root', password='', host='localhost', database='result_demo')
cur = con.cursor()

def create_table_master_table():
    cur.execute("""
            CREATE TABLE if not exists MASTER_TABLE
            (
             ROLL_NO varchar(10) NOT NULL,
             SESSION varchar(2) NOT NULL,
             SEMESTER varchar(1) NOT NULL,
             BRANCH_CODE varchar(2) NOT NULL,
             SECTION varchar(5) NOT NULL,
             SUBJECT_CODE varchar(10) DEFAULT '0',
             EXTERNAL varchar(3) DEFAULT '0',
             INTERNAL varchar(3) DEFAULT '0',
             GRADE varchar(3) DEFAULT 'A',
             PRIMARY KEY (ROLL_NO,SUBJECT_CODE)) """)
    con.commit()



def insert_in_master_table(semester, subject_no):
   for i in range(2,7):
       if(semester[0].iloc[i][3]==0):
           i=i+1
   sm=semester[0].iloc[i][3]        
   cur.execute("""insert into MASTER_TABLE
    (
    ROLL_NO,
    SESSION,
    SEMESTER,
    BRANCH_CODE,
    SECTION,
    SUBJECT_CODE,
    EXTERNAL,
    INTERNAL,
    GRADE) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
                tuple([roll_no,
                       roll_no[:2],  # session
                       sm,#semester value
                       roll_no[5:7],#branch_code
                       section,#manually entered
                       semester[0].iloc[subject_no],  # subject code
                       semester[4].iloc[subject_no],  # external
                       semester[3].iloc[subject_no],  # internal
                       semester[6].iloc[subject_no]  # grade
                       ]))
con.commit()


def update_data(semester, subject_no):
    for i in range(2,7):
       if(semester[0].iloc[i][3]==0):
           i=i+1
    sm=semester[0].iloc[i][3]
    cur.execute("""UPDATE MASTER_TABLE
                SET
                ROLL_NO = {ROLL_NO},
                SESSION = {SESSION},
                SEMESTER= {SEMESTER},
                BRANCH_CODE = {BRANCH_CODE},
                SECTION = {SECTION},
                SUBJECT_CODE ={SUBJECT_CODE},
                EXTERNAL={EXTERNAL},
                INTERNAL ={INTERNAL},
                GRADE ={GRADE}

                WHERE ROLL_NO = {ROLL_NO} AND SEMESTER = {SEMESTER}
                """.format(ROLL_NO=roll_no,
                           SESSION=roll_no[:2],  # session
                           SEMESTER=sm,  # semester value
                           BRANCH_CODE=roll_no[5:7],  # branch_code
                           SECTION=section,  # manually entered
                           SUBJECT_CODE=semester[0].iloc[subject_no],  # subject code
                           EXTERNAL=semester[4].iloc[subject_no],  # external
                           INTERNAL=semester[3].iloc[subject_no],  # internal
                           GRADE=semester[6].iloc[subject_no]))
    con.commit()



def insert_all():
    count =0
    Flag=True
    for j in b:
        count+=1
        for i in range(2,len(j)):
            try:
                insert_in_master_table(j,i)
            except:
                pass
                Flag = False
    if (Flag == False):
        print("""
            <head>
            <script>alert("Data already exist")</script>
            </head>
            """)
    else:
        print("""
            <head>
            <script>alert("Data Succesfully entered")</script>
             </head>
            """)
    redirectURL = "enter_url.php"
    print('<meta http-equiv="refresh" content="0;url=' + str(redirectURL) + '" />')

create_table_master_table()
insert_all()

cur.close()
con.close()
