from recipe.models.model_recipe import Recipe
from flask import flash, request,session, redirect, render_template
from recipe import app

@app.route('/recipes/new',methods=["GET"])
def load_create_recipe():
    recipe = {}
    return render_template("create_recipe.html",recipe_id=0,recipe=recipe)
    
@app.route('/recipes/edit/<id>',methods=["GET"])
def load_edit_recipe(id):
    data = {
        "id" : id
    }
    recipe = Recipe.getRecipeXid(data)
    return render_template("create_recipe.html",recipe_id=id,recipe=recipe)

@app.route('/recipes/<id>',methods=["GET"])
def view_recipe(id):
    data = {
        "id" : id
    }
    recipe = Recipe.getRecipeXid(data)
    return render_template("info_recipe.html",recipe=recipe)

@app.route('/delete_recipe',methods=["POST"])
def delete_recipe():
    data = {
        "id" : request.form["delete_id"]
    }
    recipe = Recipe.deleteRecipe(data)
    if(recipe == None):
        flash("The recipe was delete successfully","operation_recipe")
    else:
        flash("An error occurred while trying to delete the recipe","operation_recipe")
    return redirect('/dashboard')

@app.route('/create_recipe',methods=["POST"])
def create_recipe():
    data = {
        "name" : request.form["name_recipe"],
        "description" : request.form["description_recipe"],
        "instructions" : request.form["instructions_recipe"],
        "date_made" : request.form["date_made"],
        "thirty_minutes" : request.form["minutes"],
        "user_id" : session["id"]
    }
    recipe_id = request.form["recipe_id"]
    print(recipe_id)
    if(Recipe.verifyDataRecipe(data)):
        if(recipe_id == "0"):
            resultado = Recipe.addRecipe(data)
            if(resultado > 0):
                flash("The recipe was created successfully","operation_recipe")
                return redirect('/dashboard')
            else:
                flash("An error occurred while trying to save the recipe","operation_recipe")
                return redirect('/recipes/new')
        else:
            data["id"] = recipe_id
            resultado = Recipe.editRecipe(data)
            print(resultado)
            if(resultado == None):
                flash("The recipe was updated successfully","operation_recipe")
                return redirect('/dashboard')
            else:
                flash("An error occurred while trying to update the recipe","operation_recipe")
                return redirect('/recipes/edit/'+str(recipe_id))
    else:
        if(recipe_id == "0"):
            return redirect('/recipes/new')
        else:
            return redirect('/recipes/edit/'+str(recipe_id))