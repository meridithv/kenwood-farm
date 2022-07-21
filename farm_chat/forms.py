from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
		if golden_ticket.data != 'sammy':
			raise ValidationError(message='I\'m afraid you have the wrong secret key.  :(')

class LoginForm(FlaskForm):
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired(), Length(min=5)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')