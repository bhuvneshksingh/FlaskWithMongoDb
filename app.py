from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient


app = Flask(__name__)


title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://localhost:27017/Customer")
db = client.Customer
info = db.info

def redirect_url():
    return request.args.get('next') or \
            request.referrer or \
            url_for('index')


@app.route('/list')
def lists():
    infos = info.find()
    a1 = 'active'
    return render_template('index.html', a1=a1, infos=infos, t=title, h=heading)


@app.route('/')
@app.route('/uncompleted')
def tasks():
    infos = info.find({"active":"no"})
    a2 = 'active'
    return render_template('index.html', a2=a2, infos=infos, t=title, h=heading)


@app.route('/completed')
def completed():
    infos = info.find({"active":"yes"})
    a3 = 'active'
    return render_template('index.html', a3=a3, infos=infos, t=title, h=heading)

@app.route('/done')
def done():
    id = request.values.get("_id")
    infos = info.find({"_id":ObjectId(id)})
    if infos[0]["active"] == "yes":
        info.update_one({"_id":ObjectId(id)}, {"$set": {"active":"no"}})
    else:
        info.update_one({"_id":ObjectId(id)}, {"$set": {"active":"yes"}})
    redir = redirect_url()
    return redirect(redir)

@app.route('/action', methods=["POST"])
def add_task():
    name = request.values.get("name")
    email = request.values.get("email")
    gender = request.values.get("gender")
    joining_date = request.values.get("joining_date")
    
    info.insert_one({"name":name, "email":email, "gender":gender, "joining_date":joining_date, "active":'no'})
    return redirect("/list")

@app.route('/delete')
def delete_task():
    key = request.values.get("_id")
    info.remove({"_id":ObjectId(key)})
    return redirect('/')

@app.route('/update')
def select_update():
    id = request.values.get("_id")
    infos = info.find({"_id":ObjectId(id)})
    return render_template('update.html', infos=infos, h=heading, t=title)

@app.route('/update_task', methods=["post"])
def update_task():
    name = request.values.get("name")
    email = request.values.get("email")
    gender = request.values.get("gender")
    joining_date = request.values.get("joining_date")
    id = request.values.get("_id")
    info.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "email":email, "gender":gender, "joining_date":joining_date }})
    return redirect('/')


@app.route('/search', methods=["GET"])
def search():
    key = request.values.get("key")
    refer = request.values.get("refer")
    if (key=="_id"):
        infos = info.find({refer:ObjectId(key)})
    else:
        infos = info.find({refer:key})
    return render_template('searchlist.html', infos=infos, t=title, h= heading)


if __name__ == "__main__":
    app.run(debug=True)
