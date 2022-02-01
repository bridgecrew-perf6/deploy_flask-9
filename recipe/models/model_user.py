from recipe.config.mysqlconnection import connectToMySQL
from flask import flash
import re

NAMES_REGEX = re.compile(r'^[A-Z][a-zA-Z ]{1,80}$')
PASSWORD_REGEX = re.compile(r'^(.)*(?=\w*\d)(?=\w*[A-Z])\S{8,16}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    name_db = "db_recetas"

    def __init__(self,id,first_name,last_name,email,password,created_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_at = created_at

    @classmethod
    def addUser(cls,data):
        query = "INSERT INTO user(first_name,last_name,email,password,created_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,now());"
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def getDataUser(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        user = None
        if(len(resultado)>0):
            user = User(resultado[0]["id"],resultado[0]["first_name"],resultado[0]["last_name"],resultado[0]["email"],resultado[0]["password"],resultado[0]["created_at"])
        return user

    @classmethod
    def verifyDataUser(cls,data):
        is_valid = True
        if not NAMES_REGEX.match(data["first_name"]):
            flash("Invalid first name. Must have at least 2 characters. First letter must be capitalized","register")
            is_valid = False
        if not NAMES_REGEX.match(data["last_name"]):
            flash("Invalid last name. Must have at least 2 characters. First letter must be capitalized","register")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address","register")
            is_valid = False
        else:
            user = {
                "email" : data["email"]
            }
            resultado = cls.getDataUser(user)
            print(resultado)
            if(resultado != None):
                flash("here is already a user with the email entered","register")
                is_valid = False
        if not PASSWORD_REGEX.match(data["password"]):
            flash("Invalid password. Must contain at least one capital letter and one number. Minimum of 8 characters and a maximum of 16","register")
            is_valid = False
        if not data["password"] == data["confirm_password"]:
            flash("The confirmation password is not valid","register")
            is_valid = False
        return is_valid

    @classmethod
    def verifyDataUserLogin(cls,data):
        is_valid = True
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address","login")
            is_valid = False
        if not PASSWORD_REGEX.match(data["password"]):
            flash("Invalid password","login")
            is_valid = False
        return is_valid