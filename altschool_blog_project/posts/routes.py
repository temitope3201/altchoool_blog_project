from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from altschool_blog_project import db, login_manager
from flask_login import login_required, current_user
from altschool_blog_project.models import Post
from altschool_blog_project.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/posts/new', methods=['GET', 'POST'])
@login_required
def create_post():

    form = PostForm()
    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data
        post = Post(title = title, content= content, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Has Been Created', 'success')

        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Create Post', form = form, legend = 'Add A New Post')

@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title= post.title, post = post, legend = 'New Post' )

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    
   
    form = PostForm()

    if form.validate_on_submit():
        
        post.title = form.title.data
        post.content = form.content.data

        db.session.commit()

        flash('Your Post Has been Updated', 'success')

        return redirect(url_for('posts.post', post_id = post.id))

    elif request.method == 'GET':

        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title= post.title, form = form, legend = 'Update Post' )


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    
    else:
        db.session.delete(post)
        db.session.commit()

        flash('Your Post Has been Deleted', 'success')

        return redirect(url_for('main.home'))
