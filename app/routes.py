from app import app
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, UserCreationForm

from .models import User
from flask import flash, render_template,url_for,redirect, request


@app.route('/', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            print(username, email, password)

            # add user to database
            user = User(username, email, password)
            # print(user)

            user.saveToDB()

            return redirect(url_for('loginPage'))


    return render_template('signup.html', form = form )



@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username= form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:

                if user.password == password:
                    login_user(user)
                    flash("Successfully logged in", category="success")
                    
                else:
                    flash("Wrong password", category="danger")
            else:
                flash("This user does not exist.", category="danger")
        
    return render_template('login.html', form=form)