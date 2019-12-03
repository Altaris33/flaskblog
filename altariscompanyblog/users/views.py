#users views.py

#register user
#log in user
#log out user
#show an acccount (update account)
#sho list of user's Blog Posts

from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from altariscompanyblog import db
from werkzeug.security import generate_password_hash, check_password_hash
from altariscompanyblog.models import User, BlogPost
from altariscompanyblog.users.forms import RegistrationForm, LoginForm,UpdateUserForm
from altariscompanyblog.users.picture_handler import add_profile_pic
#from guess_language import guess_language

users = Blueprint('users',__name__)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))

#register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form)   
        

@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()  #creating a form object for login -> at this state the user already exist(register)

    if form.validate_on_submit():
        #user already exist -> query it
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log in Success')
            next = request.args.get('next')  #grabs from the session what the user was trying to access (URI) if only log in they will be sent to the home page

            if next == None or not next[0]=='/': 
                next = url_for('core.index')
            return redirect(next) 
        #else: 
        #    flash('Failure, username or password do not exist or is invalid.')     
    return render_template('login.html',form=form)   

#account (update UserForm) -> check if a picture is changed for profile pic  (picture handler and model doing)
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)  
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your user account has been updated!')    
        return redirect(url_for('users.account'))     

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)    
    return render_template('account.html',profile_image=profile_image,form=form)

# pass the username, grab the pages where he has written posts(if correct user searched and sort the search)
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)    #cycle through user posts using pages
    # first_or_404 -> helper that helps raising 404 errors is entities not found -> instead of returning a None ObjectType. 
    # None -> absence of value - Singleton 
    user = User.query.filter_by(username=username).first_or_404(description='There is no such user as {}.'.format(username))   
    # query all the blogposts where the author/user is the writer, ordered by the date 
    # for more dive into the SQLAlchemy documentation (SQL filter_by and order by to sort) ORM 
    # paginate => creates pages and allows 5 posts per page found 
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)
    

