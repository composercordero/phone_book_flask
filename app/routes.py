from app import app, db
from flask import render_template, redirect, url_for
from app.forms import SignUpForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', method =['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        address = form.address.data
    
        check_user = db.session.execute(db.select(User).where( (User.phone == phone))).scalar()
        if check_user:
            return redirect(url_for('signup'))
    
        new_user = User(first_name = first_name, last_name = last_name, phone = phone, address = address)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for(''))
    
    return render_template('signup.html', form = form)