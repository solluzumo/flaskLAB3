from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.recaptcha import RecaptchaField

class MyForm(FlaskForm):
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')