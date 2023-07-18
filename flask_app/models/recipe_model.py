from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re
from flask import flash
from flask_app.models import user_model


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
    @classmethod
    def create(cls,data):
        query = 'INSERT INTO recipes (name, description, instructions, under_30, date_cooked, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(under_30)s,%(date_cooked)s,%(user_id)s);'
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_all (cls):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        if results:
            for row in results:
                this_recipe= cls (row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = user_model.User(user_data)
                this_recipe.chef = this_user
                all_recipes.append(this_recipe)
        return all_recipes
    

    @classmethod
    def get_one (cls,data):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'

        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if results:
            row = results [0]
            this_recipe= cls (row)
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_user = user_model.User(user_data)
            this_recipe.chef = this_user
            return this_recipe
        return False
    
    @classmethod
    def delete(cls,data):
        query = " DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query ="""
            UPDATE recipes
            SET
            name = %(name)s,
            description = %(description)s,
            instructions = %(instructions)s,
            date_cooked = %(date_cooked)s,
            under_30 = %(under_30)s
            WHERE recipes.id = %(id)s;
            """ 
        return connectToMySQL(DATABASE).query_db(query,data)
        



    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data['name']) < 1:
            flash ('Name is required')
            is_valid = False
        elif len(data['name']) < 3:
            flash ('Name must have at least 3 characters')
            is_valid = False
        if len(data['description']) < 1:
            flash ('Description is required')
            is_valid = False
        elif len(data['description']) < 3:
            flash ('Description must have at least 3 characters')
            is_valid = False
        if len(data['instructions']) < 1:
            flash ('Instructions is required')
            is_valid = False
        elif len(data['instructions']) < 3:
            flash ('Instructions must have at least 3 characters')
            is_valid = False
        if len(data['date_cooked']) < 1:
            flash ('Date is required')
            is_valid = False
        if 'under_30' not in data:
            flash('Under 30 minutes is required')
            is_valid = False
        return is_valid
        