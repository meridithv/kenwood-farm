from flask import Flask, render_template, url_for
#from forms import RegistrationForm, LoginForm

app = Flask(__name__) 

'''app.config['SECRET KEY'] = '20f8ac6ebf5a6dc2842b81235d95f034'
'''

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


@app.route("/register")
def register(): 
	form = RegistrationForm() 
	return render_template('register.html', title='Sign up', form=form)


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