from flask_app.models.user import User
from flask_app.models.job import Job
from flask_app import app
from flask import render_template,redirect,request,session,flash

@app.route('/job/new')
def new_job():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    user=User.get_by_id(data)
    return render_template('add_new_job.html', user=user)

@app.route('/job/new/add', methods=['POST'])
def add_new_job():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Job.validate_job(request.form):
        return redirect('/job/new')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'location' : request.form['location'],
        'user_id' : session['user_id']
    }
    Job.save(data)
    return redirect('/dashboard')

@app.route('/job/edit/<int:id>')
def edit_job(id):
    if 'user_id' not in session:
        return redirect('/logout')
    job_data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    job=Job.get_one(job_data)
    user=User.get_by_id(user_data)
    return render_template('edit_job.html',job=job,user=user)

@app.route('/job/update', methods=['POST'])
def update_job():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Job.validate_job(request.form):
        return redirect('/dashboard')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'location' : request.form['location'],
        'id' : request.form['id']
    }
    if not Job.validate_job(request.form):
        return redirect('/dashboard')
    Job.update(data)
    return redirect('/dashboard')

@app.route('/job/<int:id>')
def view_job(id):
    if 'user_id' not in session:
        return redirect('/logout')
    job_data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    job=Job.get_one(job_data)
    user=User.get_by_id(user_data)
    user_job=Job.get_user_from_job(job_data)
    return render_template('view_job.html', job=job, user=user, user_job=user_job)

@app.route('/job/remove/<int:id>')
def remove_job(id):
    data = {
        'id':id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    Job.remove(data)
    return redirect('/dashboard')