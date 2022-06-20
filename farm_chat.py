from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__) 
app.config.update(dict(
    SECRET_KEY="20f8ac6ebf5a6dc2842b81235d95f034",
))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	username = db.Column(db.String(40), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
	password = db.Column(db.String(60), nullable = False)
	posts = db.relationship('Post', backref = "author", lazy = True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	date_posted = db.Column(db.DateTime(), nullable = False, default = datetime.utcnow)
	content = db.Column(db.Text(), nullable = False)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}'"

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


@app.route("/register", methods=['GET', 'POST'])
def register(): 
	form = RegistrationForm() 
	if form.validate_on_submit():
		flash(f'Thanks, {form.first_name.data}! You\'ve created your account.', 'success')
		return redirect(url_for('discuss'))
	return render_template('register.html', title='Sign up', form=form)


@app.route("/login")
def login(): 
	form = LoginForm() 
	return render_template('login.html', title='Log in', form=form)


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