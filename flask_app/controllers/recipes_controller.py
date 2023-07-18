from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


@app.route('/recipes')
def dashboard():
    if 'user_id' not in session: 
        return redirect ('/')
    data = {
        'id' : session ['user_id']
    }
    logged_user = User.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template ('recipes_dashboard.html', logged_user = logged_user, all_recipes=all_recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template ('recipes_new.html')

@app.route('/recipes/create', methods = ['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect ('/')
    if not Recipe.is_valid(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        **request.form,
        'user_id' : session ['user_id']
    }
    Recipe.create(recipe_data)
    return redirect ('/recipes')

@app.route('/recipes/<int:id>/view')
def view_one_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : id
    }
    one_recipe = Recipe.get_one(data)
    return render_template('recipes_one.html', one_recipe = one_recipe)

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : id
    }
    this_recipe = Recipe.get_one(data)
    if this_recipe.user_id != session ['user_id']:
        flash('This is not your recipe! Unable to delete.')
        return redirect('/recipes')
    Recipe.delete(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/edit')
def edit_recipe_form(id):
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : id
    }
    one_recipe = Recipe.get_one(data)
    if one_recipe.user_id != session ['user_id']:
        flash('This is not your recipe! Unable to edit.')
        return redirect('/recipes')
    return render_template('recipes_edit.html', one_recipe=one_recipe)

@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect ('/')
    if not Recipe.is_valid(request.form):
        return redirect(f'/recipes/{id}/edit')
    data = {
        **request.form,
        'id' : id
    }
    one_recipe = Recipe.get_one(data)
    if one_recipe.user_id != session ['user_id']:
        flash('This is not your recipe! Unable to edit.')
        return redirect('/recipes')
    Recipe.update(data)
    return redirect ('/recipes')
    