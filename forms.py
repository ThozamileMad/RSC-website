from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class JoinForm(FlaskForm):
    id_number = StringField("ID Number", validators=[DataRequired(), Length(min=13, max=13)])
    firstname = StringField("Firstname", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    mobile = StringField("Mobile", validators=[DataRequired(), Length(min=10, max=10)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    street_address = StringField("Street address", validators=[DataRequired()])
    province = SelectField("Province", choices=[
        "Eastern Cape",
        "Free State",
        "Gauteng",
        "Northern Cape",
        "Mpumalanga",
        "North West",
        "Western Cape",
        "Limpopo"
        ]
    )
    submit = SubmitField("JOIN")

class ContactForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("SEND")

class DonationForm(FlaskForm):
    amount = IntegerField("Enter Amount", validators=[DataRequired()])
    submit = SubmitField("NEXT")

                    
