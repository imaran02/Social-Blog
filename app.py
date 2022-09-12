from flask import Flask,render_template
from flask_pymongo import PyMongo,ObjectId
from flask_bcrypt import Bcrypt
# import routes

# app = Flask(__name__)

# db = mongo.db.userdata


# if __name__=="__main__":
#     app.run(debug=True)

# # import routes


from flask import Flask, request, abort

app = Flask(__name__)
app.config['SECRET_KEY']= '5791628bb0b13ce0c676dfde280ba245'
app.config['MONGO_URI']="mongodb://localhost/sbs"
mongo = PyMongo(app)

db = mongo.db.userinfo
bcrypt = Bcrypt(app)
# import declared routes
import routes

if __name__=="__main__":
    app.run(debug=True)