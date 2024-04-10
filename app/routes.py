from app import app, db
from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm
from app.models import User
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    posts =[ 
        {
            'author':{'username':'Vijay-Vaddi'},
            'body':"This is the new beginning"
        },
        {
            'author':{'username':'Obi-Wan Kenobi'},
            'body':"I have failed you Anakin"
        },
    ]
    return render_template("index.html", title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(password=form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc!='':
            return redirect(url_for("index"))
        return redirect(next_page)
    return render_template('/login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    # redirect if logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    # 
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Success!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title = 'Register User', form=form)


@app.route('/user-profile/<username>')
@login_required
def user_profile(username): #=current_user.username
    print(current_user)
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body':'Sample Post1'},
        {'author': user, 'body':'Sample Post2'},
    ]
    return render_template('user_profile.html', user=user, posts=posts)