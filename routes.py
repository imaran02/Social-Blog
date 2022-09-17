from __main__ import app
from asyncio.windows_events import NULL
from datetime import datetime
import email
from email import message
from genericpath import exists
from unicodedata import name
from urllib import request
from flask import render_template,url_for,request,flash,redirect,session
from app import bcrypt,db,postdb,mail
import pwnedpasswords
from bson.objectid import ObjectId
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_mail import Message
import os

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'imran.hashmi226@gmail.com'
app.config['MAIL_PASSWORD'] = 'wjeovbiumczcvnpf'





import smtplib, ssl
port = 587
# # port = 465
smtp_server = "smtp.gmail.com"



@app.route('/', methods=['GET'])
def home():
    data = postdb.find({}).sort('date_posted',-1)
    posts=[]
    for i in data:
        posts.append(i)
    return render_template("demo.html",posts=posts)

@app.route('/login', methods=['GET','POST'])
def logion():
    if request.method=='POST':
       email = request.form['email']
       password = request.form['password']
       userpassword = db.find_one({'email':email},{'_id':0})
       if userpassword is not None and bcrypt.check_password_hash(userpassword['password'],password):
        session["email"] = email
        flash(f'User logged in successfully','success')
        return redirect(url_for('home'))
       else:
        flash(f'Invalid Credentials','danger')
        return redirect(url_for('logion'))

    return render_template("signin.html")


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form['name']
        email= request.form['email']
        password = request.form['password']
        count = pwnedpasswords.check(password)
        if(count>1000):
            flash(f'Use Strong Password, Compromised more than 1000 times.','danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            if ((db.count_documents({'email':email}))!=0):
                flash(f'Email Id already exists','danger')
            else:
                id = db.insert_one({
            'name':name,
            'email':email,
            'password':hashed_password
                })
                flash(f'User {name} is succesfully created','success')
                return redirect(url_for('logion'))

    return render_template("signup.html")



@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")



@app.route("/post/new",methods=['GET','POST'])
def new_post():
    if request.method=='POST':
        if session['email'] is None:
            return redirect(url_for('logion'))
        else:
            title= request.form['title']
            description = request.form['description']
            uemail= session["email"]
            user = db.find_one({'email':uemail},{'_id':0,'name':1})
            username = user['name']
            id = postdb.insert_one({'email':uemail,'name':username,'title':title,
                'description':description,'date_posted':datetime.now()})
            flash('Post created succesfully','success')
            return redirect(url_for('home'))
    
    if session['email'] is None:
        return redirect(url_for('logion'))
    else:
        return render_template("create_post.html") 
        


@app.route("/post/<id>",methods=['GET','POST'])
def post(id):
    dpost = postdb.find({'_id':ObjectId(id)})
    posts=[]
    for i in dpost:
        posts.append(i)
    return render_template("post.html",posts=posts)

@app.route("/delete_post/<id>",methods=['GET','POST'])
def delete_post(id):
    postmail = postdb.find({'_id':ObjectId(id)},{'_id':0,'email':1})
    for i in postmail:
        pmail= i
    
    if session['email'] is None:
        return redirect(url_for('logion'))
    if session['email'] !=pmail['email']:
        flash(f'You are not authorized','danger')
        return redirect(url_for('home'))
    else:
        postdb.delete_one({'_id':ObjectId(id)})
        flash('Post deleted succesfully','success')
        return redirect(url_for('home'))

@app.route("/update_post/<id>",methods=['GET','POST'])
def update_post(id):
    postmail = postdb.find({'_id':ObjectId(id)},{'_id':0,'email':1})
    for i in postmail:
        pmail= i
    if session['email'] is None:
        return redirect(url_for('logion'))
    if session['email'] !=pmail['email']:
        flash(f'You are not authorized','danger')
        return redirect(url_for('home'))
    else:
        if request.method=='GET':
            update = postdb.find({'_id':ObjectId(id)})
            oldvalues = []
            for i in update:
                oldvalues.append(i)
        if request.method=='POST':
            title= request.form['title']
            description = request.form['description']
            uemail= session["email"]
            
            user = db.find_one({'email':uemail},{'_id':0,'name':1})
            username = user['name']
            postdb.delete_many({'_id':ObjectId(id)})
            id = postdb.insert_one({'email':uemail,'name':username,'title':title,
                'description':description,'date_posted':datetime.now()})
            flash('Post updated succesfully','success')
            return redirect(url_for('home'))
    return render_template("updatepost.html",posts=oldvalues)













# def get_reset_token(self, expires_sec=1800):
#     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#     return s.dumps({'email': self.id}).decode('utf-8')

# @staticmethod
# def verify_reset_token(token):
#     s = Serializer(app.config['SECRET_KEY'])
#     try:
#         email = s.loads(token)['email']
#     except:
#         return None
#     return session['email']


# def send_reset_email(user):
#     print(user)
#     s = Serializer(app.config['SECRET_KEY'], 1800)
#     token  = s.dumps({'email': user}).decode('utf-8')
#     msg = Message('Password Reset Request',
#                   sender='immu@icorestack.io',
#                   recipients=[user])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}
# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)

    # receiver_email = user
    # message = token
    # context = ssl.create_default_context()
    # with smtplib.SMTP(smtp_server, port) as server:
    #     server.ehlo()  # Can be omitted
    #     server.starttls(context=context)
    #     server.ehlo()  # Can be omitted
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)
    #     flash(f'mail sent','success')

# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     sender_email = 'imran.hashmi226@gmail.com'
#     senderpassword = 'wjeovbiumczcvnpf'
#     if request.method=='POST':
#         email= request.form['mail']
#         user = db.find_one({'email':email},{'_id':0,'email':1})
#         if user is not None:
#             s = Serializer(app.config['SECRET_KEY'], 1800)
#             token  = s.dumps({'email': user['email']}).decode('utf-8')
#             receiver_email = user['email']
#             # message = {url_for('reset_token', token=token, _external=True)}
#             message=token
#             context = ssl.create_default_context()
#             with smtplib.SMTP(smtp_server, port) as server:
#                 server.ehlo()  # Can be omitted
#                 server.starttls(context=context)
#                 server.ehlo()  # Can be omitted
#                 server.login(sender_email, senderpassword)
#                 server.sendmail(sender_email, receiver_email, message)
#         # context = ssl.create_default_context()
#         # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#         #     server.login(sender_email, senderpassword)
#         #     server.sendmail(sender_email, receiver_email, message)
#             flash('An email has been sent with instructions to reset your password.', 'info')
#             return redirect(url_for('logion'))
#     return render_template('reset_request.html')


# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     user = verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         flash(f'Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', form=form)


# def send_reset_email(user):
#     print(user)
#     s = Serializer(app.config['SECRET_KEY'], 1800)
#     token  = s.dumps({'email': user}).decode('utf-8')
# #     msg = Message('Password Reset Request',
# #                   sender='immu@icorestack.io',
# #                   recipients=[user])
# #     msg.body = f'''To reset your password, visit the following link:
# # {url_for('reset_token', token=token, _external=True)}
# # If you did not make this request then simply ignore this email and no changes will be made.
# # '''
# #     mail.send(msg)


# def get_reset_token(self, expires_sec=1800):
#     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#     return s.dumps({'email': self.email}).decode('utf-8')


@staticmethod
def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token)['email']
    except:
        return None
    return email

# def send_reset_email(user):
#     s = Serializer(app.config['SECRET_KEY'], 1800)
#     token  = s.dumps({'email': user}).decode('utf-8')
#     msg = Message('Password Reset Request',
#                   sender='imran.hashmi226@gmail.com',
#                   recipients=[user])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}
# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)


# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if request.method=='POST':
#         email= request.form['mail']
#         user = db.find_one({'email':email},{'_id':0,'email':1})
#         if user is not None:
#             s = Serializer(app.config['SECRET_KEY'], 1800)
#             token  = s.dumps({'email': user}).decode('utf-8')
#             msg = Message('Password Reset Request',
#                   sender='imran.hashmi226@gmail.com',
#                   recipients=[user])
#             msg.body = f'''To reset your password, visit the following link:
#             {url_for('reset_token', token=token, _external=True)}
# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#             mail.send(msg)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('home'))
#     return render_template('reset_request.html')








@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if request.method=='POST':
        email= request.form['mail']
        user = db.find_one({'email':email},{'_id':0,'email':1})
        if user is not None:
            s = Serializer(app.config['SECRET_KEY'], 1800)
            token  = s.dumps({'email': user['email']}).decode('utf-8')
            usere = user['email']
            msg = Message('Password Reset Request',
                  sender='imran.hashmi226@gmail.com',
                  recipients=[usere])
            msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
            mail.send(msg)
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        #     server.login(sender_email, senderpassword)
        #     server.sendmail(sender_email, receiver_email, message)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('logion'))
    return render_template('reset_request.html')




@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if session['email'] is not None:
        return redirect(url_for('home'))
    user = verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    if request.method=='POST':
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.update_one({'email':user},{'$set':{'password':hashed_password}})
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('reset_token.html')

