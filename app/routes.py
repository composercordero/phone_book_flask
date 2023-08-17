from app import app, db
from flask import render_template, redirect, url_for, flash
from app.forms import SignUpForm, LoginForm
from app.models import Contact
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods =["GET", "POST"])
def contact():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        address = form.address.data

        check_user = db.session.execute(db.select(Contact).where( (Contact.phone == phone))).scalar()
        if check_user:
            flash('A user with that username already exists', 'danger')
            return redirect(url_for('contact'))
    
        new_contact = Contact(first_name = first_name, last_name = last_name, phone = phone, address = address)
        db.session.add(new_contact)
        db.session.commit()
        flash(f'{new_contact.username} has been created', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(User).where(User.username = username)).scalar()
        if user is not None and user.check_password(password):
            login_user(user)
            flash("You have successfully logged in" , "success")
            return redirect(url_for('index'))
        
    elif form.is_submitted():
        flash("Your passwords did not match", "danger")
        return redirect(url_for('login'))
    
    return render_template('login.html', form = form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for('index'))