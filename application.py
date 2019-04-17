#!/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, url_for, request, session, redirect,Markup, flash
from flask_pymongo import PyMongo
import autofill
import os
import re
import sys ##pnkil
from functools import wraps
import time
from flask import jsonify
from random import randint
import string
import random
import password
app = Flask(__name__)
app.config["MONGO_DBNAME"] = "autofill"
app.config["MONGO_URI"] = "mongodb://ppp:PANKIL@cluster0-shard-00-00-tqm1v.mongodb.net:27017,cluster0-shard-00-01-tqm1v.mongodb.net:27017,cluster0-shard-00-02-tqm1v.mongodb.net:27017/autofill?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

mongo = PyMongo(app)
otp = 0
otp_array =[]
change_password_array = []
change_password = ''
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    email = request.args.get('email', None)
    passwor = request.args.get('password', None)
    if email in '' or passwor in '' or '@' not in email or not re.match(r'^\w+$',passwor ) or len(passwor) < 6:
        return "Invalid"
    if request.method == 'POST' or request.method == 'GET': 
        users = mongo.db.users
        login_use = users.find_one({'email' : email})
       # print(login_user)
        if login_use:
            x = login_use['pwd']
            print(password.decrypt(x[0],x[1]))
            pss = password.decrypt(x[0],x[1])
            print("decrypt " + pss)
            if (passwor == pss):
                print("HIIII")
                session['email'] = email
                session['name'] = login_use['name']
                login_user = []
                for i in login_use:
                    if(str(i) in "_id"):
                        continue
                    if "password" in str(i):
                        xx = login_use[str(i)]
                        login_user.append({str(i) : password.decrypt(xx[0],xx[1])}) 
                    else:
                        login_user.append({str(i) : login_use[str(i)]})
                print(login_user)
                return jsonify(login_user)
            else :
                message = Markup("<strong> Password is wrong </strong>")
                flash(message)
    return render_template('login.html')

@app.route('/login_website', methods=['GET','POST'])
def login_website():
    if request.method == 'POST': 
        users = mongo.db.users
        login_use = users.find_one({'email' : request.form['email']})
        if login_use:
            session['isverified'] = login_use['isverified']
            x = login_use['pwd']
            if (request.form['password'] == password.decrypt(x[0],x[1])):
                session['email'] = request.form['email']
                session['name'] = login_use['name']
                if login_use['isverified'] == 'false':
                    message = Markup("<strong>Verify your email !</strong>")
                    flash(message)
                    return redirect(url_for('verify'))
                login_user = []
                for i in login_use:
                    if(i in "_id"):
                        continue
                    login_user.append({str(i) : login_use[str(i)]})
                print(login_user)
                return render_template('index.html')
            else:
                message = Markup("<strong>Wrong Password !</strong>")
                flash(message)
        else:
            message = Markup("<strong>Not a valid user , Please signup.</strong>")
            flash(message)
    return render_template('login.html')
def email_verification(receiver):
    msg = MIMEMultipart()
    global otp
    otp = randint(1000, 9999)
    global otp_array
    otp_array.append(str(otp))
    print("otp " + str(otp))
    msg['From'] = 'autofill.sen@gmail.com'
    msg['To'] = receiver
    msg['Subject'] = 'Autofill : Verify your email'
    message = ''
    message = 'Autofill account \n\nVerify your email address\n\nTo finish setting up your Autofill account, we just need to make sure this email address is yours.\n\nTo verify your email address use this security code: ' + str(otp)+'\n\nIf you did not request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.\n\nThanks,\nThe Autofill Team'
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('autofill.sen@gmail.com', 'Autofill@123')
    mailserver.sendmail('autofill.sen@gmail.com',receiver,msg.as_string())
    mailserver.quit()
    return otp
def forget_password(receiver):
    msg = MIMEMultipart()
    global change_password
    char_set = string.ascii_uppercase + string.digits
    change_password = ''.join(random.sample(char_set*6, 6))
    global change_password_array
    change_password_array.append(change_password)
    msg['From'] = 'autofill.sen@gmail.com'
    msg['To'] = receiver
    msg['Subject'] = 'Autofill : Reset your password'
    message = ''
    message = 'Autofill account \n\nPassword reset for your Autofill account is requested.\n\nEnter this ' + change_password+' password at reset form.\n\nThanks,\nThe Autofill Team'
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('autofill.sen@gmail.com', 'Autofill@123')
    mailserver.sendmail('autofill.sen@gmail.com',receiver,msg.as_string())
    mailserver.quit()
    return change_password

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            session['email'] = request.form['email']
            email_verification(request.form['email'])
            hashpass=password.encrypt(request.form['password'])

            #print(sha256_crypt.verify("password", password))
            users.insert({'name' : request.form['first_name'] + " "+ request.form['last_name'],'firstname' : request.form['first_name'], 'lastname' : request.form['last_name'] ,'email' : request.form['email'], 'pwd' : hashpass,
            'address' : request.form['address1'] + " "+ request.form['address2'] ,'address1' : request.form['address1'],'address2' : request.form['address2'],
            'zipcode' : request.form['zipcode'],'city' : request.form['city'],
            'state' : request.form['state'],'phone' : request.form['phone_no'], 'mobile' : request.form['phone_no'],
            'isverified' : "false"
            })
            session['email'] = request.form['email']
            session['name'] = request.form['first_name']
            return redirect(url_for('verify'))
        else:
            message = Markup("<strong>That Account already exists!</strong>")
            flash(message)
        return render_template('signup.html')

    return render_template('signup.html')

@app.route('/autofill', methods=['POST', 'GET'])
def autofill_text():
    users = mongo.db.users
    url = request.args.get('url', None)
    print(url)
    #existing_user = users.find_one({'email' : session['email']})

    if(request.method == 'POST'):
        existing_user = users.find_one({'email' : session['email']})
        return render_template("autoupdate.html")
    else:
        return jsonify(autofill.func(url))
         
@app.route('/autoupdate', methods=['POST', 'GET'])
def autoupdate_text():
    idd = request.args.get('id', None)
    val = request.args.get('value', None)
    if(val in ""):
        return "null value"
    if "password" in idd:
        print(idd)
        val = password.encrypt(val)
    if(request.method == 'POST'):
        return autofill.autoupdate_texti(idd,val)
    else:
        return autofill.autoupdate_texti(idd,val)

@app.route('/details', methods=['POST', 'GET'])
def details():
    rows = {}
    users = mongo.db.users
    existing_user = users.find_one({'email' : session['email']})
    x = existing_user['pwd']
    print(x)
    if(request.method == 'GET'):
        for i in existing_user:
            if "pwd" == str(i):
                rows[str(i)] = str(password.decrypt(x[0],x[1]))
            elif "password" in str(i):
                y = existing_user[str(i)]
                rows[str(i)] = str(password.decrypt(y[0],y[1]))                 
            else:
                rows[str(i)] = str(existing_user[str(i)]) 
        #print(rows)
        return render_template("details.html",rows=rows)

    elif(request.method == 'POST'):
        #print(existing_user['email'])
        for j in existing_user:
            if(j not in "_id" and j not in "times" and j not in "isverified"):
                if j == "pwd":
                    rows[str(j)] = password.encrypt(request.form[str(j)])[0]                    
                    passw = password.encrypt(request.form[str(j)])                    
                    op = []
                    op.append(passw[0])
                    op.append(passw[1])
                    users.update({'email': existing_user['email']}, {'$set' : {'pwd' : op}})
                elif "password" in j:
                    rows[str(j)] = password.encrypt(request.form[str(j)])[0]                    
                    passw = password.encrypt(request.form[str(j)])                    
                    op = []
                    op.append(passw[0])
                    op.append(passw[1])
                    users.update({'email': existing_user['email']}, {'$set' : {str(j) : op}})
                else:
                    rows[str(j)] = str(existing_user[str(j)]) 
                    users.update({'email': existing_user['email']}, {'$set' : {str(j) : request.form[str(j)]}})
        #print(rows)
        message = Markup("<strong> Details Successfully updated.</strong>")
        flash(message)
        return redirect(url_for('details'))
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/verify', methods=['POST', 'GET'])
def verify():
    users = mongo.db.users
    existing_user = users.find_one({'email' : session['email']})
    if existing_user['isverified'] == 'false':
        if request.method == "POST":
            print(otp_array)
            print(request.form['otp'])
            if(str(request.form['otp']) in otp_array):
                otp_array.remove(str(request.form['otp']))
                users.update({'email': existing_user['email']}, {'$set' : {'isverified' : "true"}})
                return redirect(url_for('login_website'))
            else:
                message = Markup("<strong>Wrong OTP , Try again !</strong>")
                flash(message)
    else:
        redirect(url_for('login'))
    return render_template('verification.html')

@app.route('/resend', methods=['POST'])
def resend():
    if request.method == "POST":
        message = Markup("<strong>We have resent you an OTP on this email, Check your inbox.</strong>")
        flash(message)
        xx = email_verification(session['email'])
        if(xx):
            return render_template('verification.html')

@app.route('/forgetpassword', methods=['POST', 'GET'])
def forgetpassword():
    if request.method == "POST":
        session['email'] = request.form['reset_email']
        forget_password(request.form['reset_email'])
        return redirect(url_for('changedpassword'))
    return render_template('forgetpassword.html')

@app.route('/changedpassword', methods=['POST', 'GET'])
def changedpassword():
    if request.method == "POST":
        if(str(request.form['changed_password']) in change_password_array):
            change_password_array.remove(str(request.form['changed_password']))
            passw = password.encrypt(change_password)            
            opp = []
            opp.append(passw[0])
            opp.append(passw[1])
            users = mongo.db.users
            existing_user = users.find_one({'email' : session['email']})
            users.update({'email': existing_user['email']}, {'$set' : {'pwd' : opp}})
            return redirect(url_for('login_website'))
        else:
            message = Markup("<strong>Please enter the password which is sent to your registered email.</strong>")
            flash(message)
    return render_template('changepassword.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
app.secret_key = 'mysecret'

if __name__ == '__main__':  
    app.run(debug=True)
