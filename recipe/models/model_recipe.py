from recipe.config.mysqlconnection import connectToMySQL
from flask import flash
import re

NAME_REGEX = re.compile(r'^[A-Za-z ]{3,80}$')
DESCRIPTION_REGEX = re.compile(r'^(.){3,200}$')
INSTRUCTIONS_REGEX = re.compile(r'^((.)\n*){3,3000}$')
FECHA_REGEX = re.compile(r'^[1-2]{1}[9|0|1]{1}[0-9]{2}[-][0-1]{1}[0-9]{1}[-][0-3]{1}[0-9]{1}$')

class Recipe:

    name_db = "db_recetas"

    def __init__(self,id,name,thirty_minutes,description,instructions,date_made,created_at,user_id):
        self.id = id
        self.name = name
        self.thirty_minutes = thirty_minutes
        self.description = description
        self.instructions = instructions
        self.date_made = date_made
        self.created_at = created_at
        self.user_id = user_id

    @classmethod
    def getRecipes(cls):
        query = '''
                    SELECT *, (CASE WHEN (thirty_minutes = 1) THEN 'YES' ELSE 'NO' END) AS aux_thirty_minutes
                    FROM recipe;
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query)
        recipes = []
        if(len(resultado) > 0):
            for recipe in resultado:
                recipes.append(Recipe(recipe["id"],recipe["name"],recipe["aux_thirty_minutes"],recipe["description"],recipe["instructions"],recipe["date_made"],recipe["created_at"],recipe["user_id"]))
        return recipes
    
    @classmethod
    def getRecipeXid(cls,data):
        query = '''
                    SELECT *, (CASE WHEN (thirty_minutes = 1) THEN 'YES' ELSE 'NO' END) AS aux_thirty_minutes
                    FROM recipe WHERE id=%(id)s;
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        recipe = None
        if(len(resultado) > 0):
            for recipe in resultado:
                recipe = Recipe(recipe["id"],recipe["name"],recipe["aux_thirty_minutes"],recipe["description"],recipe["instructions"],recipe["date_made"],recipe["created_at"],recipe["user_id"])
        return recipe

    @classmethod
    def addRecipe(cls,data):
        query = '''
                    INSERT INTO recipe (name,thirty_minutes,description,instructions,date_made,created_at,user_id)
                    VALUES (%(name)s,%(thirty_minutes)s,%(description)s,%(instructions)s,%(date_made)s,now(),%(user_id)s)
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def editRecipe(cls,data):
        query = '''
                    UPDATE recipe SET name= %(name)s,thirty_minutes=%(thirty_minutes)s,description=%(description)s,
                    instructions=%(instructions)s,date_made=%(date_made)s,updated_at = now()
                    WHERE id = %(id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def deleteRecipe(cls,data):
        query = '''
                    DELETE FROM recipe WHERE id = %(id)s
                '''
        resultado = connectToMySQL(cls.name_db).query_db(query,data)
        return resultado

    @classmethod
    def verifyDataRecipe(cls,data):
        is_valid = True
        if not NAME_REGEX.match(data["name"]):
            flash("The recipe name is not valid. Must contain at least 3 alphabetic characters","register_recipe")
            is_valid = False
        if not DESCRIPTION_REGEX.match(data["description"]):
            flash("The description of recipe is not valid. Must contain at least 3 characters","register_recipe")
            is_valid = False
        if not INSTRUCTIONS_REGEX.match(data["instructions"]):
            flash("The instructions of recipe is not valid. Must contain at least 3 characters","register_recipe")
            is_valid = False
        if not FECHA_REGEX.match(data["date_made"]):
            flash("The date made is invalid","register_recipe")
            is_valid = False
        return is_valid