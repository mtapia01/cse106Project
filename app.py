from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import json
from flask_sqlalchemy import SQLAlchemy


# import database
# from database import db, Student

app = Flask(__name__, static_folder = 'static', template_folder = 'templates')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'

db = SQLAlchemy(app)

#id = table organization Name = student/admin/teacher's name type = student/admin/teacher
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(7), nullable=False)

#idk how but we also need to store classes into this table
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), unique=True, nullable=False)
#     #classes = db.Column()
    
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/user', methods=['POST'])
def create_student():
    if request.method == 'POST':
        requestStudent = request.get_json()
        newStudent = Users(name=requestStudent['name'], password=requestStudent['password'], type=requestStudent['type'])
        db.session.add(newStudent)
        db.session.commit()
        # jsonify({'message': 'Student added'}), 200
        return jsonify({'message': 'Student created successfully'})
    else:
        return jsonify({'error': 'Invalid request'})
    


if __name__ == '__main__':
    app.run()