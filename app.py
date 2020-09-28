from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient


app = Flask(__name__)


title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://localhost:27017/TaskManager")
db = client.TaskManager
todos = db.todo1

def redirect_url():
    return request.args.get('next') or \
            request.referrer or \
            url_for('index')


@app.route('/list')
def lists():
    todos_1 = todos.find()
    a1 = 'active'
    return render_template('index.html', a1=a1, todos=todos_1, t=title, h=heading)


@app.route('/')
@app.route('/uncompleted')
def tasks():
    todos_1 = todos.find({"done":"no"})
    a2 = 'active'
    return render_template('index.html', a2=a2, todos=todos_1, t=title, h=heading)


@app.route('/completed')
def completed():
    todos_1 = todos.find({"done":"yes"})
    a3 = 'active'
    return render_template('index.html', a3=a3, todos=todos_1, t=title, h=heading)

@app.route('/done')
def done():
    id = request.values.get("_id")
    task = todos.find({"_id":ObjectId(id)})
    if task[0]["done"] == "yes":
        todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
    else:
        todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
    redir = redirect_url()
    return redirect(redir)

@app.route('/action', methods=["POST"])
def add_task():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert_one({"name":name, "desc":desc, "date":date, "pr":pr, "done":'no'})
    return redirect("/list")

@app.route('/delete')
def delete_task():
    key = request.values.get("_id")
    todos.remove({"_id":ObjectId(key)})
    return redirect('/')

@app.route('/update')
def select_update():
    id = request.values.get("_id")
    task = todos.find({"_id":ObjectId(id)})
    return render_template('update.html', tasks=task, h=heading, t=title)

@app.route('/update_task', methods=["post"])
def update_task():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    id = request.values.get("_id")
    todos.update_one({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
    return redirect('/')


@app.route('/search', methods=["GET"])
def search():
    key = request.values.get("key")
    refer = request.values.get("refer")
    if (key=="_id"):
        todos_1 = todos.find({refer:ObjectId(key)})
    else:
        todos_1 = todos.find({refer:key})
    return render_template('searchlist.html', todos=todos_1, t=title, h= heading)


if __name__ == "__main__":
    app.run(debug=True)
