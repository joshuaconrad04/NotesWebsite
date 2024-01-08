from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
  # Make sure the User model is correctly defined
from werkzeug.security import generate_password_hash, check_password_hash

from . import db  # Make sure you have the 'db' object set up properly

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #This is what I do when I am lookin for a user in my data base by a specific value
        user = User.query.filter_by(email=email).first()
         #This is to check if the user password in the database is the same as the password that was inputted/retrieved by the get request
        if user:           
            if check_password_hash(user.password, password):
                flash("Logged in successfully! ", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else: 
                flash("Incorrect password, try again.", category ="error")
        else:
            flash("Email does not exist.",  category = "error")

    return render_template("login.html", user= current_user)



@auth.route('/logout')
#makes it so that you cannot login access this page unless logged in 
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method=="POST":
        email=request.form.get('email')
        first_Name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2=request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category = "error")
        elif len(email) < 4:
            flash('Email must be at least 2 characters long.', category='error')
            return render_template("sign_up.html")
    
        elif len(first_Name) < 2:
            flash('First Name must at least one character long.', category='error')
            return render_template("sign_up.html")
            
        elif password1 != password2:
            flash('Passwords don\'match.', category='error')
            return render_template("sign_up.html")
            
        elif len(password1)<7:
            flash('Length of password must be at least 7 characters long')
            return render_template("sign_up.html")
            
        # finally adds user to database
        else:
            #come back and test after database completion
           new_user = User(email=email, first_Name=first_Name, password=generate_password_hash(password1, method='sha256'))
           db.session.add(new_user)
           db.session.commit()
           login_user(user, remember=True)

           flash('Account created!', category='success')
           return redirect(url_for('views.home'))

            
            
    return render_template("sign_up.html", user=current_user)
