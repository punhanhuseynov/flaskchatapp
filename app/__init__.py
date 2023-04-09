from flask import Flask,render_template,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY']='SECRET'
db=SQLAlchemy(app)
login_manager=LoginManager()

login_manager.init_app(app)



from .routes import *
from .models import *