from flask import Flask,render_template,request,flash,url_for,session,redirect
from otp import genotp
from cmail import sendemail
from adminmail import adminsendmail
from adminotp import adotp
from patientidotp import patientidotp
from doctorotp import doctorotp
from doctormail import doctorsendmail
import mysql.connector
import os
mydb=mysql.connector.connect(host='localhost',
user='root',
password='root',
db='patient'
)
app=Flask(__name__)
app.secret_key="hdrfyrb"
@app.route('/',methods=['GET','POST'])
def welcome():
    return render_template('welcome.html')
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('homepage.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select email from signup')
        data=cursor.fetchall()
        cursor.execute('select mobile from signup')
        edata=cursor.fetchall()
        if(mobile,)in edata:
            flash('User already exist')
            return render_template('register.html')
        if(email,)in data:
            flash('Email address already exists')
            return render_template('register.html')
        cursor.close()
        otp=genotp()
        subject='thanks for registering to the application'
        body=f'use this otp to register {otp}'
        sendemail(email,subject,body)
        return render_template('otp.html',otp=otp,username=username,mobile=mobile,email=email,address=address,password=password)
    else:
        return render_template('register.html')

@app.route('/otp/<otp>/<username>/<mobile>/<email>/<address>/<password>',methods=['GET','POST'])
def otp(otp,username,mobile,email,address,password):
    if request.method=='POST':
        uotp=request.form['otp']
        if otp==uotp:
            cursor=mydb.cursor()
            lst=[username,mobile,email,address,password]
            query='insert into signup values(%s,%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect(url_for('login'))
        else:
            flash('Wrong otp')
            return render_template('otp.html',otp=otp,username=username,mobile=mobile,email=email,address=address,password=password)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from signup where username=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        print(count)
        if count==0:
            flash('Invalid email or password')
            return render_template('login.html')
        else:
            session['user']=username
            if not session.get(username):
                session[username]={}
            return redirect(url_for('appointment'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home'))
    else:
        flash('already logged out!')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    cursor=mydb.cursor()
    cursor.execute('select * from records')
    records=cursor.fetchall()
    return render_template('dashboard.html',records=records)

@app.route('/adminsignup',methods=['GET','POST'])
def adminsignup():
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select email from adminsignup')
        data=cursor.fetchall()
        cursor.execute('select mobile from adminsignup')
        edata=cursor.fetchall()
        print(data)
        if (mobile, ) in edata:
            flash('User already exisit')
            return render_template('adminsignup.html')
        if (email, ) in data:
            flash('Email id already exisit')
            return render_template('adminsignup.html')
        cursor.close()
        # adminotp=adotp()
        subject='thanks for registering to the application'
        body=f'use this adminotp to register {adminotp}'
        adminsendmail(email,subject,body)
        return render_template('adminotp.html',adminotp=adminotp,name=name,mobile=mobile,email=email,password=password)
    else:
        return render_template('adminsignup.html') 

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    # if session.get('admin'):
    #     return redirect(url_for('adminlogin'))
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from adminsignup where email=%s and password=%s',[email,password])
        count=cursor.fetchone()[0]
        print(count)
        if count==0:
            flash('Invalid email or password')
            return render_template('adminlogin.html')
        else:
            session['admin']=email
            return redirect(url_for('home'))
    return render_template('adminlogin.html')

@app.route('/adminlogout')
def adminlogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('adminlogin'))
    else:
        flash('already logged out!')
        return redirect(url_for('adminlogin'))

@app.route('/adminotp/<name>/<mobile>/<email>/<password>',methods=['GET','POST'])
def adminotp(adminotp,name,mobile,email,password):
    if request.method=='POST':
        uotp=request.form['adminotp']
        if adminotp==uotp:
            cursor=mydb.cursor()
            lst=[name,mobile,email,password]
            query='insert into adminsignup values(%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect(url_for('adminlogin'))
        else:
            flash('Wrong otp')
            return render_template('adminotp.html',adminotp=adminotp,name=name,mobile=mobile,email=email,password=password)
@app.route('/appointment',methods=['GET','POST'])
def appointment():
    if request.method=='POST':
        name=request.form['name']
        phone=request.form['phone']
        message=request.form['message']
        date=request.form['date']
        time=request.form['time']
        print(id,name,phone,message,date,time)
        cursor=mydb.cursor()
        cursor.execute('Insert into  appoint(patientname, phone, message, date, time) values (%s,%s,%s,%s,%s)',[name,phone,message,date,time])
        mydb.commit()
        cursor.close()
        return redirect(url_for('home'))
    else:
        return render_template('appointment.html')

@app.route('/check_in_out',methods=['GET','POST'])
def check_in_out():
    if request.method=="POST":
        id=request.form['id']
        action=request.form['action']
        valid_actions=['Check-In','Check-Out']
        if action not in valid_actions:
            flash('Invalid action.Please select a valid option.')
            return render_template('check_in_out.html')
        date=request.form['date']
        time=request.form['time']
        cursor=mydb.cursor()
        cursor.execute('Insert into checkinout(appointment_id,action,check_in_time,check_out_time) values(%s,%s,%s,%s)',[id,action,date,time])
        mydb.commit()
        cursor.close()   
    return render_template('check_in_out.html')

@app.route('/records', methods=['GET', 'POST'])
def records():
    if request.method == "POST":
        try:
            Patientname = request.form['Patientname']
            Records = request.form['Records']
            image = request.files['image']

            cursor = mydb.cursor()
            idotp = patientidotp()
            filename = idotp + '.jpg'
            cursor.execute ('insert into records (patientId,patientname, records) VALUES (%s,%s, %s)', 
                [idotp, Patientname, Records]
            )
            mydb.commit()
            path = os.path.dirname(os.path.abspath(__file__))
            static_path = os.path.join(path, 'static')
            os.makedirs(static_path, exist_ok=True)
            image.save(os.path.join(static_path, filename))

            flash("Records added successfully!")
        except KeyError as e:
            flash(f"Missing form data: {e}")
        except Exception as e:
            flash(f"An error occurred: {e}")
    return render_template('records.html')

@app.route('/updaterecords/<patientid>',methods=['GET','POST'])
def updaterecords(patientid):
    if session.get('admin'):
        print(patientid)
        cursor=mydb.cursor()
        cursor.execute('select patientname,records from records where patientid=%s',[patientid])
        records=cursor.fetchone()
        print(records)
        cursor.close()
        if request.method=="POST":
            Patientname = request.form['Patientname']
            Records = request.form['Records']
            cursor=mydb.cursor()
            cursor.execute('update records set patientname=%s, records=%s where patientid=%s',[Patientname,Records,patientid])
            mydb.commit() 
            cursor.close()
            return redirect(url_for('dashboard'))
        return render_template('updaterecords.html',records=records)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/deleterecords/<patientid>',methods=['GET','POST'])
def deleterecords(patientid):
    cursor=mydb.cursor()
    cursor.execute('delete from records where patientid=%s',[patientid])
    mydb.commit()
    cursor.close()
    path=os.path.dirname(os.path.abspath(__file__))
    static_path=os.path.join(path,'static')
    filename=patientid+'.jpg'
    os.remove(os.path.join(static_path,filename))
    flash('deleted')
    return redirect(url_for('dashboard'))

@app.route('/doctor')
def doctor():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM appoint')
    appoint = cursor.fetchall()
    cursor.execute('SELECT * FROM checkinout')
    check_in_out = cursor.fetchall()
    return render_template('doctor.html', appoint=appoint, check_in_out=check_in_out)

@app.route('/docsignup',methods=['GET','POST'])
def docsignup():
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select email from docsignup')
        data=cursor.fetchall()
        cursor.execute('select mobile from docsignup')
        edata=cursor.fetchall()
        print(data)
        if (mobile, ) in edata:
            flash('User already exisit')
            return render_template('docsignup.html')
        if (email, ) in data:
            flash('Email id already exisit')
            return render_template('docsignup.html')
        cursor.close()
        doctorotp=adotp()
        subject='thanks for registering to the application'
        body=f'use this doctorotp to register {doctorotp}'
        doctorsendmail(email,subject,body)
        return render_template('doctorotp.html',doctorotp=doctorotp,name=name,mobile=mobile,email=email,password=password)
    else:
        return render_template('docsignup.html') 

@app.route('/doclogin',methods=['GET','POST'])
def doclogin():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor()
        cursor.execute('select count(*) from docsignup where email=%s and password=%s',[email,password])
        count=cursor.fetchone()[0]
        print(count)
        if count==0:
            flash('Invalid email or password')
            return render_template('doclogin.html')
        else:
            session['admin']=email
            return redirect(url_for('home'))
    return render_template('doclogin.html')

@app.route('/doclogout')
def doclogout():
    if session.get('doctor'):
        session.pop('doctor')
        return redirect(url_for('doclogin'))
    else:
        flash('already logged out!')
        return redirect(url_for('doclogin'))

@app.route('/doctorotp/<doctorotp>/<name>/<mobile>/<email>/<password>',methods=['GET','POST'])
def doctorotp(doctorotp,name,mobile,email,password):
    if request.method=='POST':
        uotp=request.form['doctorotp']
        if doctorotp==uotp:
            cursor=mydb.cursor()
            lst=[name,mobile,email,password]
            query='insert into docsignup values(%s,%s,%s,%s)'
            cursor.execute(query,lst)
            mydb.commit()
            cursor.close()
            flash('Details registered')
            return redirect(url_for('doclogin'))
        else:
            flash('Wrong otp')
            return render_template('doctorotp.html',doctorotp=doctorotp,name=name,mobile=mobile,email=email,password=password)


app.run(debug=True)