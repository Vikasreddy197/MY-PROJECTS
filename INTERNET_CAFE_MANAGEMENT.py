
"""
Created on Fri Apr 21 23:24:34 2023

@author: KONREDDY AKSHITH REDDY
"""


import sys
import sqlite3
import datetime
import time
import random

d={}

def connection():
    conn = sqlite3.connect("cyber.db")
    return conn


def user(pc):
    heading()
    print("\n\t\t\t\t\t\t Enter anything")
    print("\t\t\t\t\t\t Enter 'end' for exit (without quotes) ")
    a=''
    while(a.lower()!='end'):
        a=input()
    conn=connection()
    print("\n\t\t\t\t\t\t YOUR RESPONSE WILL HELP US A LOT ")
    print("\n\t\t\t\t\t\t PLEASE ENTER YOUR FEEDBACK :")
    conn.execute("insert into feedback values(?,?)", (pc, input()))
    conn.commit()
    conn.close()

def User_login():
    heading()
    print("\n\t\t\t\t\t\t Login to Continue")
    sno=int(input("\n\t\t\t\t\t\t\t Enter  User Number:"))
    pas=input("\t\t\t\t\t\t\t Enter password:")
    conn = connection()
    paid=conn.execute("select logoutTime from history where sno=? and password=?",(sno,pas))
    flag=0
    for i in paid:
        for j in i:
            if(j!=None):
                print("User Number Already Used!!")
                flag=1
                break
        if(flag==1):
            break
    else:
        record=conn.execute("select sno,password from history")
        flag=0
        for i in record:
            if(sno in i and pas in i):
                flag=1
                l_in=datetime.datetime.now()
                print("\n\t\t\t\t\t\t YOU HAVE SUCCESSFULLY LOGGED IN ")
                record1=conn.execute("select pc_alloted from history where sno=? and password=?",(sno,pas))
                fl=0
                for i in record1:
                    for j in i:
                        fl=1
                        hk=j;
                        break
                    if(fl==1):
                        break
                
                conn.commit()
                conn.close()
                user(hk)
                
                conn=connection()
                
                l_out=datetime.datetime.now()
                time_diff =  l_out - l_in
                tsecs = int(time_diff.total_seconds())
                tmins = int(tsecs/60)
                conn.execute("update history set loginTime=? where sno=?", (l_in,sno))
                conn.execute("update history set logoutTime=? where sno=?", (l_out,sno))
                conn.execute("update history set timeUsed=? where sno=?", (tsecs,sno))
                conn.execute("update history set money=? where sno=?", (tsecs,sno))
                break
    conn.commit()
    conn.close()
    if(flag==0):
        print("\n\t\t\t\t\t\t Incorrect Login Credentials")
        a=int(input("Enter 1 to Re-enter details and any number to go back:"))
        if(a==1):
            User_login()

def up():
    heading()
    conn=connection()
    name=input("\t\t\t\t\t\t Enter name:")
    ic=int(input("\t\t\t\t\t\t Enter IC number:"))
    record = conn.execute("select remaining from ICcard where  ic_number=? and name=? ",(ic,name))
    flag=1
    for i in record:
        for j in i:
            
            if(j!=-1):
                k=f(name,ic)
                print("Your Balance=",k)
                print("\n\t\t\t\t\t Enter 1 to add money")
                print("\n\t\t\t\t\t Enter 2 to withdraw")
                ch=int(input("\t\t\t\t\t\t Enter your choice:"))
                if(ch==1):
                    ad=int(input("\t\t\t\t\t\t Enter Money to add:"))
                    k=k+ad
                    record = conn.execute("update ICcard set balance=? where  ic_number=?",(k,ic))
                    print("your balance =",k)
                    time.sleep(3)
                    conn.commit()
                    conn.close()
                elif(ch==2):
                    rem=int(input("\t\t\t\t\t\t Enter Money to remove:"))
                    if(rem>k):
                        print("error accessing excess money!!")
                        conn.commit()
                        conn.close()
                        time.sleep(3)
                        ic_op()
                    else:   
                        k=k-rem
                        record = conn.execute("update  ICcard set balance=? where  ic_number=?",(k,ic))
                        print("your balance =",k)
                        time.sleep(3)
                        conn.commit()
                        conn.close()
                else:
                    print("Incorrect choice")
            else:
                print("Your Card has been Expired")
                conn.commit()
                conn.close()
            flag=0
            break
        break
    if(flag==1):
        print("Sorry!You don't have an account !!")
        time.sleep(5)
        conn.commit()
        conn.close()

def f(name,ic):
    conn=connection()
    record = conn.execute("select balance from ICcard where  ic_number=? and name=? ",(ic,name))
    for i in record:
        for j in i:
            conn.commit()
            conn.close()
            return j

def bal():
    heading()
    conn=connection()
    print("\n\t\t\t\t\t Enter User's Details")
    name=input("\t\t\t\t\t\t Enter name:")
    ic=int(input("\t\t\t\t\t\t Enter IC number:"))
    j=f(name,ic)
    if(j==None):
        print("Sorry!You don't have an account !!")
    else:
        print("Your Balance=",j)
    time.sleep(5)
    conn.commit()
    conn.close()

def exp(nex,today):
    td=str(nex-today)
    for i in td:
        if(i=='0' or i=='-'):
            return -1
        else:
            return 0

def check(a,k):
    if(a in k):
        a=random.randint(1, 100000)
        check(a,k)
    else:
        return a

def apply():
    heading()
    conn = connection()
    print("\n\t\t\t\t\t Enter User's Details")
    name=input("\t\t\t\t\t\t Enter name:")
    bal=int(input("\t\t\t\t\t\t Enter deposit:"))
    phno=input("\t\t\t\t\t\t Enter Phone number:")
    record = conn.execute("select ic_number from ICcard where name=? and phno=?",(name,phno))
    flag=0
    for i in record:
        for j in i:
            if(j!=None):
                flag=1
                print("You already have an account with IC number=",j)
                time.sleep(5)
                break
        if(flag==1):
            break
    else:
        record = conn.execute("select ic_number from ICcard")
        k=[]
        a=random.randint(1, 100000)
        for i in record:
            for j in i:
                if(j!=None):
                    k.append(j)
        a=check(a,k)
        today=datetime.datetime.now()
        qwe=conn.execute("SELECT DATETIME(?, ?)",(today,'30 minutes'))
        for i in qwe:
            for j in i:
                nex=datetime.datetime.strptime(j, '%Y-%m-%d %H:%M:%S');
                break
            break
             
        conn.execute("insert into ICcard values(?,?,?,?,?,?,?)", (name,a,bal,phno,today,nex,exp(nex,today)))
        print("Congratulations on Creating an IC card with id=",a)
        time.sleep(4)
    conn.commit()
    conn.close()

def ic_op():
    heading()
    conn = connection()
    today=datetime.datetime.now()
    nex1=conn.execute("select expiry_date,ic_number from ICcard")
    for i in nex1:
        nex=datetime.datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S');
        conn.execute("update ICcard set remaining=? where ic_number=?", (exp(nex,today),i[1]))
    record = conn.execute("select name,ic_number,balance,phno from ICcard where remaining=-1")
    print("\n\n \t\t Mentioned Below are the Members whose Card validity is going to expire within 1 hr or expired-> Please Remove your account")
    print("\n\t\t name  \t  ic_number \t balance \t phno")
    flag=0
    for i in record:
        flag=1
        print("\n\t\t",end="")
        for j in i:
            print(j,end=" \t ")
    if(flag==0):
        print("\n\t\t There no persons whose validity has expired")
    conn.commit()
    conn.close()
    print("\n\t\t\t\t\t\t Enter 1 for Applying new IC card")
    print("\t\t\t\t\t\t Enter 2 for Viewing Balance")
    print("\t\t\t\t\t\t Enter 3 for Updating Balance")
    print("\t\t\t\t\t\t Enter 4 to Delete IC card")
    print("\t\t\t\t\t\t Enter 5 to View all IC card Holders")
    print("\t\t\t\t\t\t Enter 0 to go back")
    ch=int(input("\t\t\t\t\t\t Enter Your Choice:"))
    if(ch==1):
        apply()
        ic_op()
    elif(ch==2):
        bal()
        ic_op()
    elif(ch==3):
        up()
        ic_op()
    elif(ch==4):
        conn = connection()
        name=input("\t\t\t\t\t\t Enter name:")
        ic=int(input("\t\t\t\t\t\t Enter IC number:"))
        record = conn.execute("select balance from ICcard where ic_number=? and name=?",(ic,name))
        flag=1
        for i in record:
            flag=0
            for j in i:
                if(j!=0):
                    print("your remaining balance=",j)
                    print("please wait for 5 seconds ! you will be given")
                    time.sleep(5)
                conn.execute("delete from ICcard where ic_number =? and name=?",(ic,name))
                break
            break
        if(flag==1):
            print("You don't have an account!")
            time.sleep(2)
        conn.commit()
        conn.close()
        ic_op()
    elif(ch==5):
        conn = connection()
        record = conn.execute("select * from ICcard")
        print("\n\t\t(name,ic_number,balance,phno,created_on ,expiry_date ,remaining )")
        print("\n\t\t-----------------------------------------------------------------",end="")
        for i in record:
            print("\n\t\t",i)
        print("\n")
        conn.commit()
        conn.close()
        ic_op()
    elif(ch==0):
        admin()
    else:
        print("Invalid Choice")
        ic_op()

def feed():
    conn = connection()
    record = conn.execute("select * from feedback")
    print("\n\t\t PC \t Feedback")
    print("------------------------------------",end="")
    for i in record:
        print("\n\t\t",end="")
        for j in i:
            print(j,end=" \t ")
    print("\n")
    conn.commit()
    
    conn.close()

def history():
    conn = connection()
    record = conn.execute("select * from history")
    print("\n\t\t (sno,Name,Phno,Password,PC,Login time,Logout time,Time used,Money,Paid,IC_number)")
    print("\t\t -----------------------------------------------------------------------------")
    for i in record:
        print("\t\t",i)
    time.sleep(10)
    conn.commit()
    conn.close()

def free():
    heading()
    available()
    conn = connection()
    print("\n\t\t\t\t\t Enter User's Details")
    sno=int(input("\t\t\t\t\t\t Enter User Number:"))
    
    sno1=conn.execute("select max(sno) from history")
    flag=0
    for i in sno1:
        for j in i:
            if(j==None or sno>j):
                print("Invalid Details!! Please tell Correctly!")
                time.sleep(2)
                flag=1
            break
        if(flag==1):
            break
    else:
        password=input("\t\t\t\t\t\t Enter Password :")
        paid=conn.execute("select paid_through from history where sno=? and password=?",(sno,password))
        flag=0
        for i in paid:
            for j in i:
                if(j!=None):
                    print("Payment Already Done!!")
                    flag=1
                    break
            if(flag==1):
                break
        else:
            pc=conn.execute("select pc_alloted from history where sno=? and password=?",(sno,password))
            flag=0
            for i in pc:
                for j in i:
                    flag=1
                    if(j==None):
                        print("Invalid Details!! Please tell Correctly!")
                        time.sleep(2)
                    else:
                        qw=j
                        print("\n\t\t\t\t\t\t\t Time Used: ",end="")
                        pc=conn.execute("select timeUsed from history where sno=? and password=?",(sno,password))
                        flag1=0
                        for i in pc:
                            for j in i:
                                flag1=1
                                if(j==None):
                                    print("You haven't used any system so no payment!!")
                                    d[qw]=0
                                    conn.execute("update history set paid_through=? where sno=?", ('No Payment',sno))
                                    conn.execute("update history set logoutTime=? where sno=?", (0,sno))
                                    conn.commit()
                                    conn.close()
                                    time.sleep(2)
                                else:
                                    print("\n\t\t\t\t\t\t\t Time used : ",j," mins")
                                    print("\n\t\t\t\t\t\t\t Bill: ",j)
                                    conn.commit()
                                    conn.close()
                                    print("\n\t\t\t\t\t Payment through: ")
                                    print("\t\t\t\t\t\t 1) Cash ")
                                    print("\t\t\t\t\t\t 2) IC card")
                                    ch=int(input("\t\t\t\t\t Enter Your Choice:"))
                                    if(ch==1):
                                        conn = connection()
                                        conn.execute("update history set paid_through=? where sno=?", ('Cash',sno))
                                        conn.commit()
                                        conn.close()
                                        print("\n\t\tProcessing payment through Spot Cash\a\a\a");
                                        time.sleep(3)
                                        print("\n\t\tPayment Done!!");
                                        time.sleep(2)
                                        d[qw]=0
                                    elif(ch==2):
                                        conn = connection()
                                        name1=conn.execute("select name from history where sno=? and password=?",(sno,password))
                                        for i in name1:
                                            for hm in i:
                                                name=hm
                                                break
                                            break
                                        ic=int(input("\t\t\t\t\t\t Enter IC number:"))
                                        jk=f(name,ic)
                                        if(jk==None):
                                            print("Sorry!You don't have an account !!")
                                            print("\n\t\tProcessing payment through Spot Cash\a\a\a");
                                            conn.execute("update history set paid_through=? where sno=?", ('Cash',sno))
                                            time.sleep(3)
                                            print("\n\t\tPayment Done!!")
                                        else:
                                            if(jk<j):
                                                print("Sorry!You don't have enough balance in account !!")
                                                print("\n\t\tProcessing payment through Spot Cash\a\a\a");
                                                conn.execute("update history set paid_through=? where sno=?", ('Cash',sno))
                                                time.sleep(3)
                                                print("\n\t\tPayment Done!!")
                                            else:
                                                rec = conn.execute("select remaining from ICcard where  ic_number=? and name=? ",(ic,name))
                                                for i in rec:
                                                    for mk in i:
                                                        if(mk!=-1):
                                                            conn.execute("update history set paid_through=? where sno=?", ('IC Card',sno))
                                                            conn.execute("update history set ic_number=? where sno=?", (ic,sno))
                                                            conn.execute("update ICcard set balance=? where IC_number=?", (jk-j,ic))
                                                            time.sleep(3)
                                                            print("\n\t\tPayment Done!!")
                                                        else:
                                                            print("Sorry!Your card is expired !!")
                                                            print("\n\t\tProcessing payment through Spot Cash\a\a\a");
                                                            conn.execute("update history set paid_through=? where sno=?", ('Cash',sno))
                                                            time.sleep(3)
                                                            print("\n\t\tPayment Done!!")
                                                        break
                                                    break
                                        conn.commit()
                                        conn.close()
                                        d[qw]=0
                                    else:
                                        print("Invalid Choice!!")
                                        time.sleep(3)
                                break
                            if(flag1==1):
                                break 
                    break
                if(flag==1):
                    break
    

def allocat():
    heading()
    available()
    conn = connection()
    print("\n\t\t\t\t\t Free PC's")
    print("\t\t\t\t\t ---------")
    x=''
    flag=0
    for i in d:
        if(d[i]==0):
            print("\t\t\t\t\t\t",i)
            x=i
            flag=1
    if(flag==0):
        print("\n PLEASE WAIT FOR SOMETIME UNTIL A PC IS FREE")
        time.sleep(2)
    else:
        d[x]=1
        print("\n\t\t\t\t\t Enter User's Details")
        name=input("\t\t\t\t\t\t Enter Name:")
        phno=input("\t\t\t\t\t\t Enter User's Mobile Number:")
        password=input("\t\t\t\t\t\t Enter Password to login:")
        sno=conn.execute("select max(sno) from history")
        
        flag=0
        for i in sno:
            for j in i:
                flag=1
                if(j==None):
                    h=1
                else:
                    h=j+1
                break
            if(flag==1):
                break
        conn.execute("insert into history(sno,name,phno,password,pc_alloted) values(?,?,?,?,?)", (h,name,phno,password,x))
        print(name," you have been alloted ",x," User Number = ",h," Password = ",password)
        time.sleep(7)
    conn.commit()
    conn.close()

def available():
    conn = connection()
    record = conn.execute("select * from allPC")
    print("\n\t\t\t\t\t Sno \t Name \t Brand")
    print("\t\t\t\t\t ------------------------",end="")
    for i in record:
        print("\n\t\t\t\t\t ",end="")
        for j in i:
            print(j,end="  \t  ")
    print("\n")
    conn.commit()
    conn.close()
    
def delete_pc():
    conn = connection()
    heading()
    available()
    print("\n\t\t\t\t\t Enter PC Details to delete")
    na=input("\t\t\t\t\t\t Enter PC Name:")
    record1 = conn.execute("select pc_alloted from history where paid_through is NULL")
    
    for i in record1:
        if(na in i):
            conn.commit()
            conn.close()
            print("Can't Deleted! Because someone is using it right now!")
            time.sleep(2)
            break
    else:
        conn = connection()
        record = conn.execute("select name from allPC")
        flag=0
        for i in record:
            for j in i:
                if(j==na):
                    flag=1
                    d.pop(na)
                    conn.execute("delete from allPC where name=?",(na,))
                    print("Successfully Deleted a PC")
                    time.sleep(2)
                    break
        if(flag==0):
            print("\t\t\t\t\t\t\t PC not exits")
            time.sleep(2)
        conn.commit()
        conn.close()

def create_pc():
    conn = connection()
    heading()
    available()
    print("\n\t\t\t\t\t Enter PC Details")
    sno=int(input("\t\t\t\t\t\t Enter sno:"))
    name=input("\t\t\t\t\t\t Enter PC Name:")
    brand=input("\t\t\t\t\t\t Enter PC's Brand:")
    record = conn.execute("select name from allPC")
    flag=0
    for i in record:
        for j in i:
            if(j==name):
                print("\t\t\t\t\t\t\t PC already exits")
                flag=1
                time.sleep(2)
                break
    if(flag==0):
        d[name]=0
        conn.execute("insert into allPC values(?,?,?)", (sno, name, brand))
        print("Successfully Created a new PC")
        time.sleep(2)
        conn.commit()
        conn.close()
    
    
def com_op():
    heading()
    print("\n\t\t\t\t\t\t Enter 1 for Allocating PC")
    print("\t\t\t\t\t\t Enter 2 for Freeing PC")
    print("\t\t\t\t\t\t Enter 3 to Create a new PC's Space/database")
    print("\t\t\t\t\t\t Enter 4 to Delete a Fault PC")
    print("\t\t\t\t\t\t Enter 5 to View all PC's")
    print("\t\t\t\t\t\t Enter 6 to See History")
    print("\t\t\t\t\t\t Enter 7 to See Feedback")
    print("\t\t\t\t\t\t Enter 0 to go back")
    ch=int(input("\t\t\t\t\t\t Enter Your Choice:"))
    if(ch==1):
        allocat()
        com_op()
    elif(ch==2):
        free()
        com_op()
    elif(ch==3):
        create_pc()
        com_op()
    elif(ch==4):
        delete_pc()
        com_op()
    elif(ch==5):
        heading()
        available()
        com_op()
    elif(ch==6):
        history()
        com_op()
    elif(ch==7):
        feed()
        com_op()
    elif(ch==0):
        admin()
    else:
        print("Invalid Choice")
        com_op()

def admin():
    heading()
    print("\n\t\t\t\t\t\t Enter 1 for Computer Operations")
    print("\t\t\t\t\t\t Enter 2 for IC Card Operations")
    print("\t\t\t\t\t\t Enter any number to log out")
    ch=int(input("\t\t\t\t\t\t Enter Your Choice:"))
    if(ch==1):
        com_op()
    elif(ch==2):
        ic_op()
    else:
        k()

def Admin_login():
    heading()
    print("\n\t\t\t\t\t\t Login to Continue")
    name=input("\n\t\t\t\t\t\t\t Enter Admin name:")
    pas=input("\t\t\t\t\t\t\t Enter password:")
    if(name=='system' and pas=='tiger'):
        print("\n\t\t\t\t\t\t YOU HAVE SUCCESSFULLY LOGGED IN ")
        admin()
    else:
        print("\n\t\t\t\t\t\t Incorrect Login Credentials")
        a=int(input("Enter 1 to Re-enter details and any number to go back:"))
        if(a==1):
            Admin_login()
        
def heading():
    now=datetime.datetime.now()  
    st = now.strftime("%d/%m/%Y %H:%M:%S")
    print("\t\t\t\t -------------------------------------------------\t\t\t\t")
    print("\t\t\t\t|   WELCOME TO INTERNET CAFE MANAGEMENT SYSTEM    |\t\t")
    print("\t\t\t\t|    - The place where world under your fingers   |\t\t")
    print("\t\t\t\t -------------------------------------------------\t\t\t\t")
    print("\t\t\t\t ",st)



conn = connection()
conn.execute("create table if not exists allPC(sno integer,name text primary key,brand text)")
record = conn.execute("select name from allPC")
for i in record:
    for j in i:
        d[j]=0
conn.commit()
conn.close()

conn = connection()
conn.execute("create table if not exists ICcard(name text,ic_number number primary key,balance number,phno text,created_on date,expiry_date date,remaining number)")
conn.commit()
conn.close()

conn = connection()
conn.execute("create table if not exists history(sno number primary key,name text,phno text,password text ,pc_alloted text,loginTime date,logoutTime date,timeUsed date,money number,paid_through text,ic_number number)")
conn.commit()
conn.close()

conn = connection()
conn.execute("create table if not exists feedback(PC_name text,fb text)")
conn.commit()
conn.close()
def k():    
    while True:
        now=datetime.datetime.now()  
        st = now.strftime("%d/%m/%Y %H:%M:%S")
        print("\t\t\t\t -------------------------------------------------\t\t\t\t")
        print("\t\t\t\t|          INTERNET CAFE MANAGEMENT SYSTEM        |\t\t")
        print("\t\t\t\t|          --Every click you make brings you      |\t\t")
        print("\t\t\t\t|            close to our hearts                  |\t\t")
        print("\t\t\t\t -------------------------------------------------\t\t\t\t")
        print("\t\t\t\t ",st);
        print("\n\t\t\t\t\t\t Login through")
        print("\t\t\t\t\t\t\t 1-> Admin")
        print("\t\t\t\t\t\t\t 2-> User")
        print("\n\t\t\t\t\t\t Enter 0 to Close")
    
        n = int(input("\t\t\t\t\t\t Enter Your Choice:"))
        if n == 1:
            Admin_login()
            
        elif n == 2:
            User_login()
    
        elif n == 0:
            sys.exit()
    
        else:
            print("\n\t\t Selection Invalid!")
k()
