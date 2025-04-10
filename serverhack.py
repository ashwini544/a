from flask import Flask, request, redirect, url_for, render_template
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["local"]
mycol = mydb["test"]

secret = "pass123"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET','POST'])
def form():
    code = request.args.get("secret")
    if code != secret and request.method == 'GET':
        return "<h3>We don't know you</h3>"

    if request.method == 'GET':
        return render_template("form.html")
    if request.method == 'POST':
        regno = request.form.get("regno")
        username = request.form.get("username")
        clas = request.form.get("class")
        marks = request.form.get("marks")

        sid = None
        op = request.form.get("op")
        if op=="Register":
            stu = mycol.insert_one({"reg_no":regno, "username":username, "class":clas, "marks":marks})
            sid = stu.inserted_id
            return "inserted<br>id: " + str(stu.inserted_id)

        sid = request.form.get("id")
        if op=="Update":
            mycol.update_one({"_id":ObjectId(sid)}, {"$set":{"reg_no":regno, "username":username, "class":clas, "marks":marks}})
            return "updated"
        
        if op=="Delete":
            mycol.delete_one({"_id":ObjectId(sid)})
            return "deleted"
        
        if op=="Retrieve":
            stu = mycol.find_one({"_id":ObjectId(sid)})
            if stu == None:
                return "Not registered"
            student = "<h1>" + "regno: " + str(stu.get("reg_no")) + "<br>username: " + str(stu.get("username")) + "<br>class: " + str(stu.get("class")) + "<br>marks: " + str(stu.get("marks")) + "</h1>"
            return student
        client.close()
        return "Please try again"

    return redirect(url_for("form"))

