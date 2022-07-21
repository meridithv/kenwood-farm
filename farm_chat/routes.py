from flask import render_template, url_for, flash, redirect, request
from farm_chat import app, db, bcrypt
from farm_chat.forms import RegistrationForm, LoginForm
from farm_chat.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
	{
		'author': 'Meridith Viguet',
		'title': 'Welcome to the farm site!',
		'content': 'First post content lorem ipsum.',
		'date_posted': 'June 19, 2022'
	},
	{
		'author': 'John Mathews',
		'title': 'Meridith is a bad programmer',
		'content': 'She should have gone to class in 2012 lorem ipsum.',
		'date_posted': 'June 15, 2022'
	}
] 

@app.route("/")
@app.route("/discuss") 
def discuss():
	return render_template('discuss.html', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register(): 
	if current_user.is_authenticated:
		return redirect(url_for('discuss'))
	form = RegistrationForm() 

	if form.validate_on_submit():
		combined_username = form.first_name.data + form.last_name.data
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=combined_username, email=form.email.data, password=hashed_password)
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
	return redirect(url_for('discuss'))


@app.route("/tree")
@login_required
def tree():
	return render_template('tree.html', title='The Mathews/Sharvott/etc Tree')


@app.route("/account")
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file)

if __name__ == '__main__':
	app.run(debug=True)

'''
@app.route("/discuss")
	# tbd here
@app.route("/calendar")
	# tbd here
@app.route("/photos")
	# tbd here
@app.route("/familytree")
	# tbd here
'''