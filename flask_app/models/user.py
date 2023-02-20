from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import job
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re  
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'chores'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data ):
        query = """
        INSERT INTO users 
        ( first_name, last_name, email, password) 
        VALUES 
        ( %(first_name)s, %(last_name)s, %(email)s, %(password)s )
        ;"""
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for person in results:
            users.append(cls(person))
        print(users)
        return users

    @classmethod
    def get_by_email(cls,data):
        query = """SELECT * FROM users 
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])



    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * FROM 
        users WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register( user ):
        is_valid = True
        query = """SELECT * FROM users 
        WHERE email = %(email)s;"""
        results = connectToMySQL(User.db).query_db(query,user)
        if len(user['first_name']) < 2:
            flash('First name must be at least 3 characters long!')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 3 characters long!')
            is_valid = False
        if len(results) >= 1:
            flash('Email already taken!')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 Characters')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
