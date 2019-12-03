# hold a lot of organizational logic connecting blueprints together for instance
# altariscompanyblog/__init__.py
# this will lighten the code in app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

#when deploying it will be setup as an environment variable
app.config['SECRET_KEY'] = 'mysecret'

#####################
## DATABASE SETUP ###
#####################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# setting up databse and connectin' it to app
db = SQLAlchemy(app)
Migrate(app,db)

#####################
## LOGIN CONFIURATIONS
#####################
login_manager = LoginManager()

#pass it in our app to the login manager 
login_manager.init_app(app)

# Tell users what view to go to when they need to login 
login_manager.login_view = 'users.login'


#connecting the components together and register them
from altariscompanyblog.core.views import core
from altariscompanyblog.users.views import users 
from altariscompanyblog.blog_posts.views import blog_posts
from altariscompanyblog.error_pages.handlers import error_pages

# adding blueprint to register elements and connect them.
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(error_pages)