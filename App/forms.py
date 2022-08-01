from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,BooleanField,FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from App.models import User, Expense



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Sorry, this username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Sorry, this Email Address already exists! Please try a different email address')

    username = StringField(label='Your name dear user:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Your Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Your password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm your password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Your name dear user:')])
    password = PasswordField('Password', validators=[DataRequired('Your password here:')])
    submit = SubmitField(label='Sign in')



class ExpenseForm( FlaskForm):
    
    def validate_amount_minus(form,field):
        if field.data >= 0:
            raise ValidationError("This number must positive and greater than zero!")

    def validate_above_1000(form,field):
        if field.data <= 1000:
            raise ValidationError("This number must  greater than 1000!")
    
    date_of_introduction = StringField(label='Date of introduction', validators=[DataRequired("Enter date of the appearance of the expense"),Length(min=3, max=50,
    )] )
    category = StringField(label='Category', validators=[DataRequired ("Enter a type of amount"),Length(min=3, max=50,
                                )], )
    cat_id = IntegerField(label='Type of payment', validators= [DataRequired ("Enter a type of amount"), validate_above_1000], 
                                )                           
    cat_name = StringField(label='Name of payment',validators=[DataRequired("Enter a name of amount"),Length(min=3, max=50, 
                                )] )                         
    title = StringField(label='Name', validators=[DataRequired("Enter a title of your amount"), Length(min=4, max=80,
                                )],)
    amount = FloatField(label='Amount', validators=[DataRequired("Enter your amount"), validate_amount_minus], )

    description = StringField(label='Description', validators=[DataRequired("Enter your description here"), Length(min=4, max=200,
                                )],)

    unexpected = BooleanField('Unexpected')

    paid = BooleanField("Unpaid")

    date_of_payment = StringField(label='Date of payment', validators=[DataRequired("Enter date of payment"),Length(min=3, max=50,
                               )] )



class DeleteExpenseForm(FlaskForm):
    submit = SubmitField(label='Expense delete!')

class ModifyExpenseForm(FlaskForm):
    submit = SubmitField(label='Expense modify!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(label="Old Password", validators=[DataRequired()])
    new_password = PasswordField(label="New Password", validators=[Length(min=6),DataRequired()])
    new_password2 = PasswordField(label="Confirm new password", validators=[EqualTo('new_password'),DataRequired()])
    submit = SubmitField(label="Change Password")

class ChangeEmailForm(FlaskForm):
    email = StringField(label="New email", validators=[Email(),DataRequired()])
    password = PasswordField(label="Confirm by password", validators=[Length(min=6),DataRequired()])
    submit = SubmitField(label="Change Email")