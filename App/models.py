from sqlalchemy import Integer
from App import db, login_manager, bcrypt
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField,  DateField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, Email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=0)
    Expenses = db.relationship('Expense', backref='User_expenses', lazy=True)   


    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}PLN"


    
    def password(self):
        return self.password 


    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


    def registration_mail(self):
        msg = Message("Account creation", sender='testbautrel111@gmail.com', recipients=[self.email_address])
        msg.body = (f'Your account has been created. Your are welcome dear, {self.username} .')
        mail.send(msg)


    def change_password(self, input_password):
        self.password_hash = bcrypt.generate_password_hash(input_password).decode('utf-8')
        db.session.commit()


def change_email(self, input_email):
    self.email_address = input_email
    db.session.commit()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    date_of_introduction = db.Column(db.String, default = "11.22.94")
    category = db.Column(db.String(100), nullable=False )
    cat_id = db.Column(db.Integer, primary_key = True, unique = True)
    cat_name = db.Column(db.String(50), nullable=False)
    title = db.Column (db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column (db.Text(150))
    unexpected = db.Column (db.Boolean)
    paid = db.Column(db.Boolean)
    date_of_payment = db.Column(db.String, default = "11.22.94")
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    

    def __repr__(self):
        return f'Item {self.category, self.title}'




    def self(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()


    def delete(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()




   

    

    

