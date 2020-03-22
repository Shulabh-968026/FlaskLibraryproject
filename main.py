from flask import Flask,session,url_for,redirect,render_template,request
from flask_mail import Mail,Message
import pymysql
import json
app=Flask(__name__)
mail=Mail(app)
app.secret_key='super user key'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'user@gmail.com'
app.config['MAIL_PASSWORD'] = 'user'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
@app.route("/index")
def index(em):
   msg = Message('Hello', sender = 'senderemail', recipients = ['recevieremial'])
   msg.body = "thankyou for joining for world largest library site.we hope you injoy it. "
   mail.send(msg)
   return render_template('addlibrarian.html', msg='data is successfully inserted')

@app.route('/')
def welcome():
    return render_template('librarylogin.html')
@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
@app.route('/autherror')
def autherror():
    return render_template('autherror.html')
@app.route('/adminhome')
def adminhome():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return render_template('admintemplete.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/librarianhome')
def librarianhome():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return render_template('addlibrarian.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/dellibrarian')
def dellibrarian():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return render_template('deletelibrarian.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/edtlibrarian')
def edtlibrarian():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return render_template('editlibrarian.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/addbook')
def addbook():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='librarian':
            return render_template('addbooks.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/issbook')
def issbook():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='librarian':
            return render_template('issuebooks.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/rtubook')
def rtubook():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='librarian':
            return render_template('returnbook.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/pchange')
def changepassword():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='librarian':
            return render_template('changepassword.html')
    else:
        return redirect(url_for('autherror'))
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        conn=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            db='library',
            autocommit=True
        )
        cur=conn.cursor()
        sql="select *from logindata where email='"+email+"' and password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if n==1:
            data=cur.fetchone()
            utype=data[2]
            session['usertype']=utype
            session['email']=email
            if utype=='admin':
                return redirect(url_for('adminhome'))
            elif utype=='librarian':
                return render_template('hospitaltemplete.html')
        else:
            return render_template('librarylogin.html',msg="email or password incorrect")
    else:
        return redirect(url_for('welcome'))
@app.route('/librarian',methods=['GET','POST'])
def librarian():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                name=request.form['name']
                password=request.form['password']
                cpassword=request.form['conformpassword']
                email=request.form['email']
                address=request.form['address']
                city=request.form['city']
                contact=request.form['contact']
                usertype = 'librarian'
                conn=pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur=conn.cursor()
                if password==cpassword:
                    sql1="insert into librariandata values('"+name+"','"+password+"','"+cpassword+"','"+email+"','"+address+"','"+city+"','"+contact+"')"
                    sql2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
                    cur.execute(sql1)
                    cur.execute(sql2)
                    n=cur.rowcount
                    m=cur.rowcount
                    if n==1 and m==1:
                        return redirect(url_for('index(email)'))
                    else:
                        return render_template('addlibrarian.html',msg="data is not inserted successfully")
                else:
                    return render_template('addlibrarian.html', msg="password not matching")
            else:
                return redirect(url_for('librarianhome'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/viewlibrarian')
def viewlibrarian():
    if 'usertype' in session:
        utype=session['usertype']
        if utype=='admin':
            conn=pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                db='library',
                autocommit=True
            )
            cur=conn.cursor()
            sql="select *from librariandata"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('viewlibrarian.html',data=data)
            else:
                return render_template('viewlibrarian.html',msg="data not found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/deletelibrarian',methods=['GET','POST'])
def deletelibrarian():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                email=request.form['email']
                conn=pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur=conn.cursor()
                sql1="delete from librariandata where email='"+email+"'"
                sql2="delete from logindata where email='"+email+"'"
                cur.execute(sql1)
                cur.execute(sql2)
                n=cur.rowcount
                m=cur.rowcount
                if n==1 and m==1:
                    return render_template('deletelibrarian.html',msg="data is delete")
                else:
                    return render_template('deletelibrarian.html',msg="data not deleted")
            else:
                return redirect(url_for('dellibrarian'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/editlibrarian',methods=['GET','POST'])
def editlibrarian():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                email=request.form['email']
                conn=pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="select *from librariandata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('editlibrarian1.html',data=data)
                else:
                    return render_template('editlibrarian.html',msg="this email is not exits")
            else:
                return redirect(url_for('edtlibrarian'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/editlibrarian1',methods=['GET','POST'])
def editlibrarian1():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                name = request.form['name']
                #password = request.form['password']
                #cpassword = request.form['conformpassword']
                email = request.form['email']
                address = request.form['address']
                city = request.form['city']
                contact = request.form['contact']
                conn=pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="update  librariandata set name='"+name+"',address='"+address+"',city='"+city+"',contact='"+contact+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('editlibrarian1.html',msg='data change successfully')
                else:
                    return render_template('editlibrarian1.html',msg='data is not successfully change')
            else:
                 return redirect(url_for('autherror'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/addbooks',methods=['GET','POST'])
def addbooks():
    if 'usertype' in session:
        utype=session['usertype']
        if utype=='librarian':
            if request.method=='POST':
                bookid=request.form['bookid']
                name=request.form['name']
                auther=request.form['auther']
                publisher=request.form['publisher']
                quantity=request.form['quantity']
                issuebooks=request.form['issuebooks']
                date=request.form['date']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="insert into addbooks values('"+bookid+"','"+name+"','"+auther+"','"+publisher+"','"+quantity+"','"+issuebooks+"','"+date+"')"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('addbooks.html',msg="book is added successfully")
                else:
                    return render_template('addbooks.html',msg="book is not added")
            else:
                return redirect(url_for('addbook'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/viewbooks')
def viewbooks():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='librarian':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                db='library',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from addbooks"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('viewbooks.html',data=data)
            else:
                return render_template('viewbooks.html',msg="no books found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/issuebook',methods=['GET','POST'])
def issuebook():
    if 'usertype' in session:
        utype=session['usertype']
        if utype=='librarian':
            if request.method=='POST':
                bookid=request.form['bookid']
                sid=request.form['studentid']
                sname=request.form['studentname']
                scontact=request.form['studentcontact']
                date=request.form['date']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="select *from addbooks where bookid='"+bookid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    data=cur.fetchone()
                    num1=int(data[4])
                    num2=int(data[5])
                    if num1>num2 and num1!=0:
                        num2=num2+1
                        sql1="update addbooks set issue='"+str(num2)+"' where bookid='"+bookid+"'"
                        sql2="insert into issuebook values('" + bookid + "','" + sid + "','" + sname + "','" + scontact + "','" + date + "')"
                        cur.execute(sql1)
                        n=cur.rowcount
                        cur.execute(sql2)
                        m=cur.rowcount
                        if n==1 and m==1:
                            return render_template('issuebooks.html',data=sname)
                    else:
                        return render_template('issuebooks.html',msg="this book is last book so this book not issue")
                else:
                    return render_template('issuebooks.html',msg="please check your bookid or student id")
            else:
                return redirect(url_for('issbook'))
        else:
            return redirect(url_for('autherror'))
    else:
         return redirect(url_for('autherror'))
@app.route('/viewissbooks')
def viewissbooks():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='librarian':
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                db='library',
                autocommit=True
            )
            cur = conn.cursor()
            sql="select *from issuebook"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return render_template('viewissuebooks.html',data=data)
            else:
                return render_template('viewissuebooks.html',msg="no books found")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/returnbook',methods=['GET','POST'])
def returnbook():
    if 'usertype' in session:
        utype = session['usertype']
        if utype == 'librarian':
            if request.method == 'POST':
                bookid = request.form['bookid']
                sid = request.form['studentid']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="delete from issuebook where bookid='"+bookid+"' and studentid='"+sid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    sql1="select *from addbooks where bookid='"+bookid+"'"
                    cur.execute(sql1)
                    m=cur.rowcount
                    if m==1:
                        data=cur.fetchone()
                        num1=int(data[4])
                        num2=int(data[5])
                        if num1>num2 and num2!=0:
                            num2=num2-1
                            sql1 = "update addbooks set issue='" + str(num2) + "' where bookid='" + bookid + "'"
                            cur.execute(sql1)
                            p = cur.rowcount
                            if p==1:
                                return render_template('returnbook.html', data=sid)
                else:
                    return render_template('returnbook.html', msg="please check your bookid and student id")
            else:
                return redirect(url_for('rtubook'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/changepass',methods=['GET','POST'])
def changepass():
    if 'usertype' in session:
        ut=session['usertype']
        email=session['email']
        if ut=='librarian':
            if request.method=='POST':
                password=request.form['password']
                cpassword=request.form['cpassword']
                conn = pymysql.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='',
                    db='library',
                    autocommit=True
                )
                cur = conn.cursor()
                if password==cpassword:
                    sql="update logindata set password='"+password+"'where email='"+email+"'"
                    cur.execute(sql)
                    m=cur.rowcount
                    sql1 = "update librariandata set password='" + password + "',cpassword='" + cpassword + "' where email='" + email + "'"
                    cur.execute(sql1)
                    n = cur.rowcount
                    if m==1 and n==1:
                        return render_template('changepassword.html',msg="password successfully change")
                    else:
                        return render_template('changepassword.html',msg="password not change")
                else:
                    return render_template('changepassword.html', msg="password not change")
            else:
                return redirect(url_for('changepassword'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
if __name__=="__main__":
    app.run(debug=True)
