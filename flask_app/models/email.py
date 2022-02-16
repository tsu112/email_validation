from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Email:
    db = "email_validation"

    def __init__(self, data):
        self.id = data['id']
        self.email_address = data['email_address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO emails (email_address) VALUES (%(email_address)s);"
        results = connectToMySQL(
            Email.db).query_db(query, data)
        return results

    @staticmethod
    def validate_email(email):
        is_valid = True
        query = "SELECT * FROM emails WHERE email_address = %(email_address)s"
        results = connectToMySQL(Email.db).query_db(query, email)
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid = False
        if not EMAIL_REGEX.match(email['email_address']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails"
        emails = []
        results = connectToMySQL(Email.db).query_db(query)
        for row in results:
            emails.append(cls(row))
        return emails

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM emails WHERE id=%(id)s;"
        results = connectToMySQL(Email.db).query_db(query, data)
        return results
