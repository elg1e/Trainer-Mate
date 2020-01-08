import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/post')
def post():
    return render_template("post.html",
    categories=mongo.db.categories.find())

@app.route('/add_post', methods=["POST"])
def add_post():
    posts = mongo.db.posts
    form_data = request.form.to_dict()
    posts.insert_one(request.form.to_dict())
    url_map = {'Recipes': 'recipes', 'Workout Routines': 'workout', 'Meal Plans': 'meal'}
    return redirect(url_for(url_map[form_data['category_name']]))

@app.route('/workout')
def workout():
    return render_template("workout.html",
    posts=mongo.db.posts.find({'category_name': "Workout Routines"}))

@app.route('/meal')
def meal():
    return render_template("meal.html",
    posts=mongo.db.posts.find({'category_name': "Meal Plans"}))

@app.route('/recipes')
def recipes():
    return render_template("recipes.html",
    posts=mongo.db.posts.find({'category_name': "Recipes"}))

@app.route('/edit_posts/<posts_id>')
def edit_posts(posts_id):
    the_posts = mongo.db.posts.find_one({"_id": ObjectId(posts_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editposts.html', post=the_posts, categories=all_categories)

@app.route('/update_posts/<posts_id>', methods=["POST"])
def update_posts(posts_id):
    posts = mongo.db.posts
    posts.update( {'_id': ObjectId(posts_id)},
    {
    'plan_name':request.form.get('plan_name'), 
    'category_name':request.form.get('category_name'), 
    'workout_description':request.form.get('workout_description'), 
    })
    form_data = request.form.to_dict()
    url_map = {'Recipes': 'recipes', 'Workout Routines': 'workout', 'Meal Plans': 'meal'}
    return redirect(url_for(url_map[form_data['category_name']]))

@app.route('/delete_posts/<posts_id>')
def delete_posts(posts_id):
    mongo.db.posts.remove({'_id': ObjectId(posts_id)})
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(host=os.environ.get('IP','0.0.0.0'),
            port=int(os.environ.get('PORT','5000')),
            debug=False)