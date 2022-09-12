# from flask import render_template
# from app import app

# @app.route("/")
# def index():
#     return "working"
#     # return render_template("index.html")

from __main__ import app
import email
from urllib import request
from flask import render_template,url_for,request,flash,redirect
from app import bcrypt,db



posts = [
    {
        'author': 'Imran',
        'title': 'Social Blogging Site',
        'content': 'Login and Registartion done with DataBase connectivity',
        'date_posted': 'September 12, 2022'
    },
    {
        'author': 'Shireen',
        'title': 'Book Management Site',
        'content': 'Login , Registration with connectivity and can see Bookdetails as well',
        'date_posted': 'September 11, 2022'
    }
]





@app.route('/', methods=['GET'])
def home():
    return render_template("demo.html",posts=posts)

@app.route('/login', methods=['GET','POST'])
def logion():
    if request.method=='POST':
       email = request.form['email']
       password = request.form['password']
       userpassword = db.find_one({'email':email},{'_id':0,'password':1})
       print(bcrypt.check_password_hash(userpassword['password'],password))
       if bcrypt.check_password_hash(userpassword['password'],password):
        flash(f'User logged in successfully','success')
        return redirect(url_for('home'))


    return render_template("signin.html")


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form['name']
        email= request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        id = db.insert_one({
            'name':name,
            'email':email,
            'password':hashed_password
        })
        flash(f'User {name} is succesfully created','success')
        return redirect(url_for('logion'))

    return render_template("signup.html")