import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from farm_chat import app, db, bcrypt
from sqlalchemy import desc
from farm_chat.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from farm_chat.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/discuss") 
@login_required
def discuss():
	posts = Post.query.order_by(desc(Post.date_posted)).all()
	return render_template('discuss.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register(): 
	if current_user.is_authenticated:
		return redirect(url_for('discuss'))
	form = RegistrationForm() 

	if form.validate_on_submit():
		combined_username = form.first_name.data + form.last_name.data
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=combined_username, first_name=form.first_name.data,
		last_name=form.last_name.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Thanks, {form.first_name.data}! You\'ve created your account. You may now log in.', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Sign up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login(): 
	if current_user.is_authenticated:
		return redirect(url_for('discuss'))
	form = LoginForm() 
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first() 
		# Check that the entered email is in the database and they entered
		# something that matches the password on file.
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('discuss'))
		else:
			flash('Sorry, that didn\'t work. Double-check your e-mail and password.', 'danger')

	return render_template('login.html', title='Log in', form=form)
 

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route("/tree")
@login_required
def tree():
	return render_template('tree.html', title='The Mathews/Sharvott/etc Tree')

@app.route("/calendar")
@login_required
def calendar():
	return render_template('calendar.html', title='The Farm Calendar')


@app.route("/photos")
@login_required
def photos():
	return render_template('photos.html', title='Farm photos')

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_filename = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
	form_picture.save(picture_path)

	return picture_filename

@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()

	if form.first_name.data and form.last_name.data:
		combined_new_username = form.first_name.data + form.last_name.data
	elif form.first_name.data:
		combined_new_username = form.first_name.data + current_user.last_name
	elif form.last_name.data:
		combined_new_username = current_user.first_name + form.last_name.data
	else:
		combined_new_username = current_user.username

	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.username = combined_new_username
		current_user.email = form.email.data
		db.session.commit()
		flash(f'Thanks, {form.first_name.data}! Your account has been updated.', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
		form.email.data = current_user.email

	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Thanks! Your message has been posted to everyone.')
		return redirect(url_for('discuss'))
	return render_template("create_post.html", title="New Post", form=form)
	

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('discuss'))

if __name__ == '__main__':
	app.run(debug=True)

