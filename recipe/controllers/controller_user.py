
from recipe.models.model_recipe import Recipe
from recipe.models.model_user import User
from flask import flash, request,session, redirect, render_template
from flask_bcrypt import Bcrypt
from recipe import app

bcrypt = Bcrypt(app)

@app.route('/')
def load_initial():
    return render_template('index.html')

@app.route('/dashboard')
def load_dashboard():
    if 'id' in session:
        recipes = Recipe.getRecipes()
        return render_template('dashboard.html',recipes=recipes)
    else:
        return redirect('/')

@app.route('/register_user',methods=["POST"])
def register_user():
    user = {
        "first_name" : request.form["input_first_name"],
        "last_name" : request.form["input_last_name"],
        "email" : request.form["input_email"],
        "password" : request.form["input_password"],
        "confirm_password" : request.form["input_confirm_password"]
    }
    if(User.verifyDataUser(user)):
        user["password"] = bcrypt.generate_password_hash(request.form["input_password"])
        resultado = User.addUser(user)
        if(resultado > 0):
            session["name"] = request.form["input_first_name"]
            session["id"] = resultado
            return redirect('/dashboard')
        else:
            flash("An error occurred while trying to save the data","register")
            return redirect('/')
    else:
        return redirect('/')

@app.route('/login',methods=["POST"])
def login():
    user = {
        "email" : request.form["input_email_login"],
        "password" : request.form["input_password_login"]
    }
    if(User.verifyDataUserLogin(user)):
        resultado = User.getDataUser(user)
        if(resultado != None):
            if bcrypt.check_password_hash(resultado.password,user["password"]):
                session["name"] = resultado.first_name
                session["id"] = resultado.id
                return redirect('/dashboard')
            else:
                flash('Invalid credentials',"login")
                return redirect('/')
        else:
            flash("User does not exist","login")
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect('/')