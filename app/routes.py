from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import  LoginForm, AddressForm
from app.models import User, Address
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from app.forms import AddressForm, RegisterForm, LoginForm



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        first_name = form.data.get('first_name')
        last_name = form.data.get('last_name')
        email = form.data.get('email')
        password = form.data.get('password')
    

        new_user = User(first_name=first_name, last_name=last_name,email=email, password=password)


        db.session.add(new_user)
        db.session.commit()
        print(form.data)
        return redirect(url_for('login'))

    return render_template('register.html', form=form )

if __name__ == '__main__':
    app.run(debug=True)