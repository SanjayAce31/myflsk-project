from flask import Flask,render_template,request,redirect,url_for,flash,session

#we are going to import the sqlite3

import sqlite3 

#we are going to import flask session

from flask_session import Session

#we are importing datetime

from datetime import datetime

app=Flask(__name__)

#we are going to make a secret key

app.secret_key='power_ranger'
app.config['SESSION_TYPE']='filesystem'
Session(app)

#we are giving power to the admin 
ADMIN_CREDENTIALS={
    'Admin':'nagu1',
    'Admin_2':'nagu2'
}

#we are going to connect the database
def iniatialisedb():
    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE  IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT NOT NULL,
        Mail TEXT NOT NULL,Date TEXT NOT NULL
        )""")
    conn.commit()
    conn.close()
    


@app.route("/")
def index():
    return render_template('index.html')


#we are going to configure with post settings from the html page

@app.route('/submit',methods=['POST'])
def submit():
    name=request.form['name']
    email=request.form['mail']
    dateq=request.form['date']
    
    appointment_date=datetime.strptime(dateq,'%Y-%m-%d')
    current_date=datetime.now()
    
    #We are doing some date verifications
    
    if appointment_date<current_date:
        flash("Error,how can the appointment date be in  the past")
        return redirect(url_for('index.html'))
    
    #connection to the database
    
    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute('insert into users(Name,Mail,Date) values(?,?,?)',(name,email,dateq))
    conn.commit()
    conn.close()
    
    flash(f"{name}your appointment was confirmed on {dateq} .A Confirmation mail will be sent to you")
    
    #we are again redirecting to the index page
    
    return redirect(url_for('index'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        #we are validating the username and password
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['logged_in']=True
            flash('Successfully logged in')
            return redirect(url_for('result'))
        else:
            flash('Invalid Credentials,please try again')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in',None)
        flash('You have been logged out')
        return redirect(url_for('login'))
    

@app.route('/result')
def result():
    if not session.get('logged_in'):
        flash('You need to log in to access this page')
        return redirect(url_for('login'))
    
    conn=sqlite3.connect('database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()
    
    return render_template('result.html', data=data)

if __name__=='__main__':
    iniatialisedb()
    app.run(debug=True)