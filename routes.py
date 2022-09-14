from __main__ import app
from asyncio.windows_events import NULL
from datetime import datetime
import email
from genericpath import exists
from unicodedata import name
from urllib import request
from flask import render_template,url_for,request,flash,redirect,session
from app import bcrypt,db,sessionv,postdb
import pwnedpasswords
from bson.objectid import ObjectId
from flask_login import current_user



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
       userpassword = db.find_one({'email':email},{'_id':0,'password':1})
       if bcrypt.check_password_hash(userpassword['password'],password):
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

        if "email" not in session:
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
    return render_template("create_post.html")


@app.route("/post/<id>",methods=['GET','POST'])
def post(id):
    if "email" not in session:
        return redirect(url_for('logion'))
    else:
        dpost = postdb.find({'_id':ObjectId(id)})
        posts=[]
        for i in dpost:
            posts.append(i)
    return render_template("post.html",posts=posts)


@app.route("/delete_post/<id>",methods=['GET','POST'])
def delete_post(id):
    if "email" not in session:
        return redirect(url_for('logion'))

    else:
        dpost = postdb.delete_one({'_id':ObjectId(id)})
        flash('Post deleted succesfully','success')
        return redirect(url_for('home'))


@app.route("/update_post/<id>",methods=['GET','POST'])
def update_post(id):
    if "email" not in session:
        return redirect(url_for('logion'))
    else:
        if request.method=='GET':
            print(id)
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