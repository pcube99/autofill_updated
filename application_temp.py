#!/usr/bin/env python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, url_for, request, session, redirect,Markup, flash
from flask_pymongo import PyMongo
import autofill
import os
import re
import sys ##
from functools import wraps
import time
from flask import jsonify
import password
from random import randint
import string
import random
import password
myapp = Flask(__name__)
myapp.config["MONGO_DBNAME"] = "autofill"
myapp.config["MONGO_URI"] = "mongodb://ppp:PANKIL@cluster0-shard-00-00-tqm1v.mongodb.net:27017,cluster0-shard-00-01-tqm1v.mongodb.net:27017,cluster0-shard-00-02-tqm1v.mongodb.net:27017/autofill?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

mongo = PyMongo(myapp)
otp = 0
otp_array =[]
change_password_array = []
change_password = ''
@myapp.route('/')
def index():
    return 'index1'
@myapp.route('/login', methods=['GET','POST'])
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
            pss =password.decrypt(x[0],x[1])
            if (passwor == pss):
                session['email'] = email
                session['name'] = login_use['name']
                login_user = []
                for i in login_use:
                    if(i in "_id"):
                        continue
                    
                    login_user.append({str(i) : login_use[str(i)]})
                return "successfully login"
            else :
                message = Markup("<strong> Password is wrong </strong>")
                flash(message)
    return "failed login"

@myapp.route('/login_website', methods=['GET','POST'])
def login_website():
    if request.method == 'POST': 
        users = mongo.db.users
        login_use = users.find_one({'email' : request.form['email']})
        if login_use:
            session['isverified'] = login_use['isverified']
            x = login_use['pwd']
            if (request.form['pwd'] == password.decrypt(x[0],x[1])):
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
    otp_array.append(str(otp))
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

@myapp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})

        if existing_user is None:
            session['email'] = request.form['email']
            email_verification(request.form['email'])
            hashpass=password.encrypt(request.form['pwd'])
            users.insert({'name' : request.form['first_name'],'lastname' : request.form['last_name'] ,'email' : request.form['email'], 'pwd' : hashpass,
            'address' : request.form['address1'],'address1' : request.form['address2'],
            'zipcode' : request.form['zipcode'],'city' : request.form['city'],
            'state' : request.form['state'],'no' : request.form['phone_no'],
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

@myapp.route('/autofill', methods=['POST', 'GET'])
def autofill_text():
    users = mongo.db.users
    url = request.args.get('url', None)
    email = request.args.get('email', None)
    passwor = request.args.get('password', None)
    existing_user = users.find_one({'email' : email})
    if(request.method == 'POST'):
        existing_user = users.find_one({'email' : email})
        return render_template("autoupdate.html")
    else:
        if email in '' or passwor in '' or '@' not in email or not re.match(r'^\w+$',passwor ) or len(passwor) < 6:
            return "Invalid"
        users = mongo.db.users
        login_use = users.find_one({'email' : email})
        if login_use:
            x = login_use['pwd']
            pss = password.decrypt(x[0],x[1])
            if (passwor == pss):
                return "success"
            else:
                return "wrong password or email"
        else:
            return 'wrong login'
            
@myapp.route('/autoupdate', methods=['POST', 'GET'])
def autoupdate_text():
    users = mongo.db.users
    email = request.args.get('email', None)
    passwor = request.args.get('password', None)
    idd = request.args.get('id', None)
    val = request.args.get('value', None)
    user_v = users.find_one({'email' : email})
    if user_v:
        x=user_v['pwd']
        pss = password.decrypt(x[0],x[1])
        print(pss)
        if(passwor==pss):
            return "success"
        else: 
            return "wrong password or email"

    else:
        return 'wrong login'
@myapp.route('/details', methods=['POST', 'GET'])
def details():
    rows = {}
    email = request.args.get('email', None)
    passwor = request.args.get('password', None)
    if request.method == 'POST' or request.method == 'GET': 
        if email in '' or passwor in '' or '@' not in email or not re.match(r'^\w+$',passwor ) or len(passwor) < 6:
            return "Invalid"
        users = mongo.db.users
        login_use = users.find_one({'email' : email})
    # print(login_user)
        if login_use:
            x = login_use['pwd']
            pss = password.decrypt(x[0],x[1])
            if (passwor == pss):
                login_user = []
                for i in login_use:
                    if(i in "_id"):
                        continue
                    if "password" in i:
                        xx = login_use[str(i)]
                        login_user.append({str(i) : xx})
                    else:
                        login_user.append({str(i) : login_use[str(i)]})
                        x = login_use['pwd']
                        for i in login_use:
                            if str(i) in "password":
                                rows[str(i)] = str(x)
                            else:
                                rows[str(i)] = str(login_use[str(i)]) 
                        #print(rows)
                        return "success"
            else:
                return "wrong password or email"
        else:
            return 'wrong login'
@myapp.route('/logout')
def logout():
	session.clear()
	return "logouted"

@myapp.route('/help')
def help():
    return render_template('help.html')
@myapp.route('/verify', methods=['POST', 'GET'])
def verify():
    users = mongo.db.users
    email = request.args.get('email', None)
    #print(email)
    passwor = request.args.get('password', None)
    en_otp= request.args.get('otp', None)
    #print(en_otp)
    existing_user = users.find_one({'email' : email})
    if existing_user:
        print("true")
    else:
        return "invalid login"
    if existing_user['isverified'] == 'false':
        if request.method == "GET":
            otp_array={"2421","3421","5421","6421"}
            print(otp_array)
            print(en_otp)
            if(str(en_otp) in otp_array):
                return 'verified'
            else:
                return "wrong otp"
    else:
        return "already verified"
    #return render_template('verification.html')

@myapp.route('/resend', methods=['POST', 'GET'])
def resend():
    if request.method == "POST":
        message = Markup("<strong>We have resent you an OTP on this email, Check your inbox.</strong>")
        flash(message)
        email_verification(session['email'])
    return render_template('verification.html')

@myapp.route('/forgetpassword', methods=['POST', 'GET'])
def forgetpassword():
    if request.method == "POST":
        session['email'] = request.form['reset_email']
        forget_password(request.form['reset_email'])
        return redirect(url_for('changedpassword'))
    return render_template('forgetpassword.html')

@myapp.route('/changedpassword', methods=['POST', 'GET'])
def changedpassword():
    #if request.method == "POST":
        new_pass=request.args.get('reset_pass', None)
        change_password_array={"654321"}
        if(str(new_pass) in change_password_array):
            #change_password_array.remove(str(request.form['changed_password']))
            #passw = password.encrypt(change_password)
            #opp = []
            #opp.append(passw[0])
            #opp.append(passw[1])
            #users = mongo.db.users
            #existing_user = users.find_one({'email' : session['email']})
            #users.update({'email': existing_user['email']}, {'$set' : {'password' : opp}})
            return "password changed"
        else:
            return "enter the password which is sent to your registered email"	
            #message = Markup("<strong>Please enter the password which is sent to your registered email.</strong>")
            #flash(message)
    #return render_template('changepassword.html')

@myapp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
myapp.secret_key = 'mysecret'

if __name__ == '__main__':  
    myapp.run(debug=True)