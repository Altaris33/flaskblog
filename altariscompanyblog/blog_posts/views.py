#blog posts views
from flask import render_template,url_for,flash,request,redirect,Blueprint
from flask_login import current_user,login_required
from altariscompanyblog import db
from altariscompanyblog.models import BlogPost
from altariscompanyblog.blog_posts.forms import BlogPostForm
#from guess_language import guess_language

blog_posts = Blueprint('blog_posts',__name__)

#views ->
# creating a blog post
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        # add a language field to the post model and migrate/update the database
        #language = guess_language(form.post.data)
        #if language = 'UNKNOWN' or len(language) > 5:
        #    language = ''
        blog_post = BlogPost(title=form.title.data,text=form.text.data,user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)  

# blog post view of list -> treat the id passed as an integer, not a String
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # query the table to make sure an integer is passed and not another data type - avoid confusion - query whether or not this post exist
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',
                            title=blog_post.title,
                            date=blog_post.date,
                            post=blog_post)

# update
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
def update(blog_post_id):

    #make sure that the current author is the user so that he cannot delete or update posts from another user
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    # forbidden access - abort function provided by Flask to handle errors
    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm() 

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id)) 

    # pass back the old blog post info so they can start again with the old text and title 
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html',title='Updating',form=form)          

# delete
@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = BlogPost.query.get_or_404(blog_post_id)

    #same check for deleting a post
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))    

    # no template returned -> this will be handled by a bootstrap delete button instead
