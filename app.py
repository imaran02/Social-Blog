from flask import Flask,render_template,session
from flask_pymongo import PyMongo,ObjectId
from flask_bcrypt import Bcrypt
from flask_session import Session
# from flask_login import LoginManager

from flask import Flask, request, abort

app = Flask(__name__)
app.config['SECRET_KEY']= '5791628bb0b13ce0c676dfde280ba245'
app.config['MONGO_URI']="mongodb://localhost/sbs"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
mongo = PyMongo(app)

db = mongo.db.userinfo
postdb = mongo.db.postinfo
bcrypt = Bcrypt(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
sessionv = Session(app)

# import declared routes
import routes

if __name__=="__main__":
    app.run(debug=True)