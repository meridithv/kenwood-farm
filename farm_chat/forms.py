from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from farm_chat.models import User

class RegistrationForm(FlaskForm):
	first_name = StringField('First name or nickname',
		validators = [DataRequired(), Length(min=2)])

	last_name = StringField('Last name', validators = [DataRequired(), Length(min=2)])

	email = StringField('Email', validators = [DataRequired(), Email()])

	password = PasswordField('Password', validators = [DataRequired(), Length(min=5)])
	confirm_password = PasswordField('Confirm password',
		validators = [DataRequired(), EqualTo('password', 'Sorry––your passwords above don\'t match.')])

	golden_ticket = StringField('And the secret key?', validators =[DataRequired()])

	submit = SubmitField('Join Kenwood online!')

	def validate_email(self, email):
		existing_email = User.query.filter_by(email=email.data).first()
		if existing_email is not None:
			raise ValidationError(message='We already have that email in our records. Have you tried signing in yet?')

	def validate(self):
		rv = FlaskForm.validate(self)
		if not rv:
			return False

		desired_username = self.first_name.data + self.last_name.data
		existing_user = User.query.filter_by(username=desired_username).first()
		if existing_user is not None:
			flash('We already have your full name on file. Try signing in!')
			return False

		return True

	def validate_golden_ticket(self, golden_ticket):
		if golden_ticket.data != 'perch':
			raise ValidationError(message='I\'m afraid you have the wrong secret key.  :(')

class LoginForm(FlaskForm):
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired(), Length(min=5)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')

class AddEventForm(FlaskForm):
	name = StringField('What\'s your event called?', validators = [DataRequired()])
	content = StringField('Describe your event', validators = [DataRequired()])
	start = DateTimeLocalField('Starts when?', format='%Y-%m-%dT%H:%M',  validators = [DataRequired()])
	end = DateTimeLocalField('Ends when?', format='%Y-%m-%dT%H:%M', validators = [DataRequired()])
	submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
	first_name = StringField('First name or nickname',
		validators = [DataRequired(), Length(min=2)])

	last_name = StringField('Last name', validators = [DataRequired(), Length(min=2)])

	email = StringField('Email', validators = [DataRequired(), Email()])

	picture = FileField('Profile picture', validators = [FileAllowed(['jpg','jpeg','png'])])

	submit = SubmitField('Update your account')


	def validate(self):
		rv = FlaskForm.validate(self)
		if not rv:
			return False

		desired_new_username = self.first_name.data + self.last_name.data
		if desired_new_username != current_user.username:
			taken = User.query.filter_by(username=desired_new_username).first()
			if taken:
				flash('Someone\'s already signed up with that name. Maybe it was you?')
				return False

		return True


	def validate_email(self, email):
		if email.data != current_user.email:
			taken = User.query.filter_by(email=email.data).first()
			if taken:
				raise ValidationError('Someone\'s already made an account with that email...you, perhaps.')

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Post')

