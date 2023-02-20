from flask_app.models.user import User
from flask_app.models.job import Job
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,redirect,request,session,flash

@app.route('/')
def index():
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users = users)

@app.route('/register/user', methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    print(request.form)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password' : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def success():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(data)
    all_jobs = Job.get_all()
    my_jobs = Job.get_my_jobs(data)
    return render_template('dashboard.html', user=user, all_jobs=all_jobs, my_jobs=my_jobs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')