import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'TrainerMate'
app.config["MONGO_URI"] = 'mongodb+srv://root:root123@myfirstcluster-rieqe.mongodb.net/TrainerMate?retryWrites=true&w=majority'

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
    posts.insert_one(request.form.to_dict())
    return redirect(url_for('home'))

@app.route('/workout')
def workout():
    return render_template("workout.html",
    posts=mongo.db.posts.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP','0.0.0.0'),
            port=int(os.environ.get('PORT','8000')),
            debug=True)