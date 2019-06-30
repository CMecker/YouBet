from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Event

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Unvalid username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Unvalid email address.')

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class EventRegistrationForm(FlaskForm):

    def validate_eventname(self, eventname):
        event = Event.query.filter_by(eventname=eventname.data).first()
        if event is not None:
            raise ValidationError('Unvalid eventname.')

    eventname = StringField('Eventname', validators=[DataRequired()])
    chll = StringField('Challenger')
    time_to_bet = DateField('TimeToBet', format='%Y-%m-%d', validators=[DataRequired()])
    about_event = TextAreaField('Desricption', validators=[Length(min=0, max=140)])
    submit = SubmitField('Create')

class EventValidationForm(FlaskForm):

    def validate_eventname(self, eventname):
        event = Event.query.filter_by(eventname=eventname.data).first()
        if event is not None:
            raise ValidationError('Unvalid eventname.')

    eventname = StringField('Eventname', validators=[DataRequired()])
    winner = StringField('Winner')
    submit = SubmitField('Create')

class EventBetForm(FlaskForm):

    def __init__(self, original_username, *args, **kwargs):
        super(EventBetForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Unvalid username.')
    
    username = StringField('Challenger')
    betonloose = BooleanField('Bet on Loose')
    amount = IntegerField('Amount')
    submit = SubmitField('Make Your Bet')

class GetCoinForm(FlaskForm):

    def __init__(self, original_username, *args, **kwargs):
        super(GetCoinForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


    amount = IntegerField('Amount')
    submit = SubmitField('Give urself some money')

class EditProfileForm(FlaskForm):

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Unvalid username.')
    
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('Desricption', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
    

class PostForm(FlaskForm):
    post = TextAreaField('Post it', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
