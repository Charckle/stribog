# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField
from flask_wtf.file import FileField, MultipleFileField, FileAllowed, FileRequired

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import BooleanField, IntegerField, StringField, SelectField, PasswordField, \
     HiddenField, SubmitField, validators # BooleanField


# Import Form validators
from wtforms.validators import ValidationError

#email verification
import re
import os.path


class Target(FlaskForm):
    target_index = HiddenField('id', [validators.InputRequired(message='Dont fiddle around with the code!')])
    
    name = StringField('Ime naslovnika', [validators.InputRequired(message='Moraš specificirati ime dogodka'),
                                             validators.Length(max=128)])    

    email = StringField('Emailnaslovnika', [validators.InputRequired(message='Specify the admin email'),
                                             validators.Length(max=128)]) 
    
    active = SelectField(u'Activen?:', [
            validators.InputRequired(message='Specificiraj, če je aktiven')], 
                             choices=[('0', 'No'), ('1', 'Yes')])    

    submit = SubmitField("Dodaj dogodek")
    
    
class Configuration(FlaskForm):
    instance_name = StringField('Instance name', [validators.InputRequired(message='Specify the instance name'),
                                             validators.Length(max=128)])    
    admin_email = StringField('Admin email', [validators.InputRequired(message='Specify the admin email'),
                                             validators.Length(max=128)]) 
    
    emails = SelectField(u'Email Notifications:', [
            validators.InputRequired(message='Set if sending email notifications')], 
                             choices=[('0', 'No'), ('1', 'Yes')])
    
    send_analitycs_to_admin = SelectField(u'Admin analitycs:', [
            validators.InputRequired(message='Specify admin analitics')], 
                             choices=[('0', 'No'), ('1', 'Yes')])

    source_check_interval = IntegerField('Source check interval', [validators.InputRequired(message='Specify the check interval')])
    
    smtp_server = StringField('SMTP server', [validators.InputRequired(message='Specify a smtp server'),
                                             validators.Length(max=128)]) 
    
    smtp_port = StringField('SMTP port', [validators.InputRequired(message='Specify the SMTP port'),
                                             validators.Length(max=128)]) 
    
    smtp_sender_email = StringField('SMTP sender email', [validators.InputRequired(message='Specify the smtp sender email'),
                                             validators.Length(max=128)]) 
    
    smtp_password = StringField('SMTP password', [validators.InputRequired(message='Specify the smtp password'),
                                             validators.Length(max=128)])     
    
    topic = StringField('Notification topic', [validators.InputRequired(message='Specify the notification topic'),
                                             validators.Length(max=128)])   
    
    message = StringField('Email Message', [validators.InputRequired(message='Specify the message in the email'),
                                             validators.Length(max=128)])
    
    on_no_memory_send_one = SelectField(u'If first run/restart, send latest?:', [
            validators.InputRequired(message='Moraš specificirati velikost dogodka')], 
                             choices=[('0', 'Dont send'), ('1', 'Send'),])
    
    logging_level = SelectField(u'Logging Level:', [
            validators.InputRequired(message='Define a logging lvl')], 
                             choices=[('DEBUG', 'DEBUG'), ('INFO', 'INFO'), 
                                      ('WARNING', 'WARNING'), ('ERROR', 'ERROR'),
                                      ('CRITICAL', 'CRITICAL')])      

    submit = SubmitField("Dodaj dogodek")


class Login(FlaskForm):
    username_or_email = StringField('Username or Email', [validators.InputRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [validators.InputRequired(message='Must provide a password.')])
    remember = BooleanField()
    
    submit = SubmitField('Login')


 
form_dicts = {"Target": Target,
              "Configuration": Configuration,
              "Login": Login
              } 
