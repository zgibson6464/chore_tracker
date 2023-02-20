from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Job:
    db = 'chores'
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = []
        self.user_job = []
        self.user_jobs = []

#CREATE

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO chores
        ( title, 
        description, 
        location, 
        user_id )
        VALUES ( %(title)s, 
        %(description)s,
        %(location)s, 
        %(user_id)s )
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

#READ 

    @classmethod
    def get_all(cls):
        query = """
        SELECT * 
        FROM chores
        JOIN users
        ON chores.user_id=users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_jobs = []
        if not results:
            return results
        for this_job in results:
            new_job = cls(this_job)
            this_user = {
                'id':this_job['users.id'],
                'first_name':this_job['first_name'],
                'last_name':this_job['last_name'],
                'email':this_job['email'],
                'password':this_job['password'],
                'created_at':this_job['created_at'],
                'updated_at':this_job['updated_at']
            }
            new_job.user=user.User(this_user)
            all_jobs.append(new_job)
        return all_jobs

    @classmethod
    def get_my_jobs(cls, data):
        query = """
        SELECT *
        FROM chores
        WHERE user_id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        my_jobs = []
        for this_job in results:
            this_users_jobs = cls(this_job)
            this_users_job = {
                'id':this_job['id'],
                'title':this_job['title'],
                'location':this_job['location'],
                'description':this_job['description'],
                'user_id':this_job['user_id'],
                'created_at':this_job['created_at'],
                'updated_at':this_job['updated_at']
            }
            this_users_jobs.user_jobs=Job(this_users_job)
            my_jobs.append(this_users_jobs)
        return my_jobs

    @classmethod
    def get_one(cls,data):
        query = """
        SELECT * FROM chores
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_user_from_job(cls,data):
        query = """
        SELECT * 
        FROM chores
        JOIN users
        ON chores.user_id=users.id
        WHERE chores.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        one_job = []
        if not results:
            return results
        for this_job in results:
            this_user_job = cls(this_job)
            this_user = {
                'id':this_job['users.id'],
                'first_name':this_job['first_name'],
                'last_name':this_job['last_name'],
                'email':this_job['email'],
                'password':this_job['password'],
                'created_at':this_job['created_at'],
                'updated_at':this_job['updated_at']
            }
            this_user_job.user_job=user.User(this_user)
            one_job.append(this_user_job)
        return one_job[0]


    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM chores
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

#UPDATE

    @classmethod
    def update(cls,data):
        query = """
        UPDATE chores 
        SET 
        title=%(title)s, 
        description=%(description)s,
        location=%(location)s, 
        updated_at=NOW() 
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

#DELETE

    @classmethod
    def remove(cls,data):
        query = """
        DELETE FROM chores
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_job(job):
        is_valid = True
        if len(job['title']) < 1:
            flash('Must include Title')
            is_valid = False
        if len(job['description']) < 1:
            flash('Must include a description')
            is_valid = False
        if len(job['location']) < 1:
            flash('Must include a Location')
            is_valid = False
        return is_valid