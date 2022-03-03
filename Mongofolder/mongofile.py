from flask import Flask, render_template,request
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

#setup mongo connection with database
app.config['MONGO_URI']="mongodb://localhost:27017/shows_db"
mongo = PyMongo(app)

#connect to collection
tv_shows = mongo.db.tv_shows

#READ
@app.route("/")
def index():
    #find all items in db and save to a variable
    all_shows = list(tv_shows.find())

    return render_template('index.html',data=all_shows)
#@app.route("/insert")
#def insertt():
#CREATE
@app.route("/create", methods=["POST", "GET"])

def create_func():
    if request.method=="POST":
        data = request.form 

        post_data = {'name':data['name'], 
                     'seasons': data['seasons'], 
                     'duration': data['duration'], 
                     'date_added':datetime.datetime.utcnow()}

        tv_shows.insert_one(post_data)

        return "<p>Successfully Created.</p>"
    else:
        return render_template("form.html")

@app.route("/update", methods=["POST", "GET"])

def update_fun():
    if request.method=="POST":
        update = request.form 

        to_update = {'name':update['to_update']}

        post_update = {"$set": {'name':update['name'], 
                     'seasons': update['seasons'], 
                     'duration': update['duration'], 
                     'date_added':datetime.datetime.utcnow()}}
        
        tv_shows.updateOne(to_update,post_update)

        return "<p>Successfully updated.</p>"
    else:
        return render_template("updateform.html")

   
@app.route("/delete")
def deletee():
    del_show = tv_shows.delete_one({'name':'Money Heist'})
    return render_template('delete.html',data=del_show)
if __name__ == "__main__":
    app.run(debug=True)