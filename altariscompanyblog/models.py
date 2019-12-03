
#user models and blog post model
from altariscompanyblog import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin  #allows us to user is_authenticated, is_allowed etc...
from datetime import datetime
# setting up the user model and authentication 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png') #default image as default since users must have an image 
    email = db.Column(db.String(64),unique=True,index=True)  #SQL constraints
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    #last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #password_confirm = db.Column(db.StringField)
    posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email= email
        self.username = username
        self.password_hash = generate_password_hash(password)  #hashing the password when the user creates it ( constructor password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)  

    def __repr__(self):
        return f"Username {self.username}"      

class BlogPost(db.Model):
    __tablename__ = 'blogposts'

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(160),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
        

    def __repr__(self):
        return f"Post ID: {self.id} --- Date: {self.date} --- {self.title}"    






