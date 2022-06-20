from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
	first_name = StringField('First name or nickname',
		validators = [DataRequired(), Length(min=2)])

	last_name = StringField('Last name', validators = [DataRequired(), Length(min=2)])

	# username = first_name + last_name

	email = StringField('E-mail', validators = [DataRequired(), Email()])

	password = PasswordField('Password', validators = [DataRequired(), Length(min=5)])
	confirm_password = PasswordField('Confirm password',
		validators = [DataRequired(), EqualTo('password')])

	golden_ticket = "Meridith is kewl"

	golden_ticket_confirmed = StringField('And the secret key?',
		validators =[DataRequired(), EqualTo(golden_ticket)])

	submit = SubmitField('Join Kenwood online!')

class LoginForm(FlaskForm):
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired(), Length(min=5)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Log in')