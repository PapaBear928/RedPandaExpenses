
from App import app, db
from werkzeug.utils import secure_filename
from flask import flash, render_template, url_for,redirect,flash
from App.models import Expense, User
from App.forms import RegisterForm, LoginForm, ExpenseForm, DeleteExpenseForm, ModifyExpenseForm
from flask_login import login_user, logout_user,login_required
import os, random




#imagepath = (r"")


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('main.html')
   
   
@app.route('/review_your_expenses')
@login_required
def review_your_expenses():
    delete_form = DeleteExpenseForm
    modify_form = ModifyExpenseForm
    expenses = Expense.query.all()

    return render_template('review_your_expenses.html', expenses = expenses , modify_form=modify_form, delete_form=delete_form)


@app.route('/register',  methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Your account was created successfully! Now, you can logged in as {user_to_create.username}')
        return redirect(url_for('review_your_expenses'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}. It makes panda sad :( .', category='dangers')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are pretty welcome on board, dear: {attempted_user.username}', category='success')
            return redirect(url_for('review_your_expenses'))
        else:
            flash('Hey! This data are not match:( ) Please try again', category='danger')

    return render_template('login.html', form=form)


@login_required
@app.route('/add_another_expense' , methods=['GET', 'POST'])
def add_another_expense():

    form = ExpenseForm()
    
    if form.validate_on_submit():
        expense_to_create = Expense(
                            date_of_introduction = form.date_of_introduction.data,
                            category = form.category.data,
                            cat_id = form.cat_id.data,
                            cat_name = form.cat_name.data,
                            title = form.title.data,
                            amount = form.amount.data,
                            description = form.description.data,
                            unexpected = form.unexpected.data,
                            paid = form.paid.data,
                            date_of_payment = form.paid.data)
                            
        db.session.add(expense_to_create) 
        db.session.commit()
        expense_to_create
        flash(f'Your expense was added successfully!')
    else:
        flash('Hey! This data are not match:( ) Please try again', category='danger')

    

    return render_template('add_another_expense.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password_page():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password_correction(attempted_password=form.old_password.data):
            current_user.change_password(form.new_password.data)
            flash(f'Password has been changed', category="success")
            return redirect(url_for('panel_page'))
        else:
            flash('Wrong password')
    return render_template('change_password.html', form=form)


@app.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_page():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.check_password_correction(attempted_password=form.password.data):
            current_user.change_email(form.email.data)
            flash(f'Email has been changed to {current_user.email_address}', category="success")
            return redirect(url_for('panel_page'))
        else:
            flash('Wrong password')

    return render_template('change_email.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out. Bye bye!", category='info')
    return redirect(url_for("home_page"))


@app.route('/about')
def about_page():
    
    
    return render_template("about.html")

@login_required
@app.route('/panda_pictures')
def panda_pictures():

    images = os.listdir('App/static')
    images = ['/' + file for file in images]
    pictures = random.sample(images,k=1)

    return render_template('panda_pictures.html', pictures=pictures)
     
 