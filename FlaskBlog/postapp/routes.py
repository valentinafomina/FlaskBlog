from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from FlaskBlog import db
from FlaskBlog.models import Post
from FlaskBlog.postapp.forms import PostForm
from FlaskBlog.postapp.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/all")
@login_required
def postfeed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=5)
    post_iter = 1
    return render_template('home.html', posts=posts, post_iter=post_iter)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            post = Post(title=form.title.data, content=form.content.data,
                        author=current_user, post_image=image_file)
            db.session.add(post)
            db.session.commit()
            flash('Post is published!', 'success')
            return redirect(url_for('posts.postfeed'))
        else:
            post = Post(title=form.title.data, content=form.content.data,
                        author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Post is published!', 'success')
            return redirect(url_for('posts.postfeed'))
    return render_template('create_post.html',
                           title='New post', form=form, legend='New post')


@posts.route("/post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        flash('Post is updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post',
                           form=form, legend='Update post')


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.postfeed'))


