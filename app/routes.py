from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import ContactForm, SignUpForm, LoginForm, UpdateForm, ModifyForm
from app.models import Contact, User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/my_contacts')
def my_contacts():
    contacts = db.session.execute(db.select(Contact).where(Contact.user_id == current_user.id)).scalars().all() 
    # SELECT FROM TABLE contact WHERE user.id LIKE current_user.id
    return render_template('my_contacts.html', contacts = contacts)

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    form = ModifyForm()
    contacts = db.session.execute(db.select(Contact).where(Contact.author == current_user)).scalars().all()
    if form.validate_on_submit():
        contact_id = form.contact_id.data
        return redirect(url_for('update_contact', contact_id = contact_id))
    return render_template('modify.html', contacts = contacts, form=form)

@app.route('/contact', methods =["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        address = form.address.data

        check_user = db.session.execute(db.select(Contact).where((Contact.phone == phone))).scalar()
        if check_user and check_user.author == current_user:
            flash(f'A user named {check_user.first_name} with that phone number already exists in your Phone Book', 'danger')
            return redirect(url_for('contact'))
    
        new_contact = Contact(first_name = first_name, last_name = last_name, phone = phone, address = address, user_id = current_user.id)
        db.session.add(new_contact)
        db.session.commit()
        flash(f'{new_contact.first_name} has been created', 'success')
        return redirect(url_for('index'))
    
    return render_template('contact.html', form = form)

@app.route('/update/<contact_id>', methods =["GET", "POST"])
def update_contact(contact_id):
    form = UpdateForm()
    current_contact = db.session.get(Contact, contact_id)

    if form.validate_on_submit():
        current_contact.first_name = form.first_name.data
        current_contact.last_name = form.last_name.data
        current_contact.phone = form.phone.data
        current_contact.address = form.address.data

        if current_contact.author != current_user:
            flash(f'You cannot update this contact', 'danger')
            return redirect(url_for('my_contacts'))

        db.session.commit()
        flash(f'{current_contact.first_name} has been updated', 'success')
        return redirect(url_for('index'))
    
    return render_template('update.html', form = form, current_contact = current_contact)

@app.route('/delete', methods = ['GET', 'POST', 'DELETE'])
def delete():
    form = ModifyForm()
    contacts = db.session.execute(db.select(Contact).where(Contact.author == current_user)).scalars().all()
    contact = db.session.get(Contact, form.contact_id.data)
    # if Contact(contact_to_delete) is None:
    #     flash(f'Contact with an ID of {contact_to_delete} does not exist', 'danger')
    if form.validate_on_submit() and contact.author == current_user:
        db.session.delete(contact)
        db.session.commit()
        flash(f'{contact.first_name} {contact.last_name} has been deleted from your list.', 'success')
        return redirect(url_for('my_contacts'))
    return render_template('delete.html', contacts = contacts, form=form) 

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.session.execute(db.select(User).where(User.username==username)).scalar()
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

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalar()
        if check_user:
            flash('A user with that username already exists', 'danger')
            return redirect(url_for('signup'))
        
        new_user = User(first_name = first_name, last_name = last_name, username = username, email = email, password = password)

        db.session.add(new_user)
        db.session.commit()
        flash(f'{new_user.username} has been created', 'success')

        login_user(new_user)
  
        return redirect(url_for('index'))
    
    return render_template('signup.html', form=form)