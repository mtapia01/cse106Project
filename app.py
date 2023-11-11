from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_cors import CORS
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'dbs', 'users.db')
db = SQLAlchemy(app)

CORS(app)

class Users(db.Model, UserMixin):
    UserId = db.Column(db.Integer, primary_key=True)
    FirstLastName = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(120), nullable=False)
    Type = db.Column(db.Integer, nullable=False, default=1)  # Student, Teacher, Admin

class Classes(db.Model):
    ClassID = db.Column(db.Integer, primary_key=True)
    ClassName = db.Column(db.String(80), nullable=False)
    Instructor = db.Column(db.Integer, db.ForeignKey('users.id'))
    MeetingTime = db.Column(db.String(80), nullable=True)
    EnrolledStudents = db.Column(db.Integer)
    MaxStudents = db.Column(db.Integer)

class CourseRegistration(db.Model):
    UserIdFK = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    ClassIDFK = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    Grade = db.Column(db.Float, nullable=True)

# Create the database tables
#db.create_all()


# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # The login route's name
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



@app.route('/all-courses', methods=['GET'])
def get_all_courses():
    # Query the database to get all course information
    courses = Classes.query.all()

    # Create a list to store course data
    course_list = []

    # Iterate through the courses and append data to the list
    for course in courses:
        course_data = {
            'ClassId': course.ClassID,
            'ClassName': course.ClassName,
            'Instructor': course.Instructor,  # Assuming this is the instructor's name
            'MeetingTime': course.MeetingTime
        }
        course_list.append(course_data)

    # Render the HTML template and pass the course list
    return render_template('all_courses.html', courses=course_list)


@app.route('/register', methods=['GET'])
def display_registration():
    return render_template('registration.html')

@app.route('/', methods=['GET'])
def display_login():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/student')
def student():
    # Implement student functionality here
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    # Implement teacher functionality here
    return render_template('teacher.html')

# @app.route('/teacher/classes')
# def teacher_classes():
#     if 'user_id' in session and session['user_type'] == 2:  # Ensure the user is a teacher (user type 2)
#         instructor_id = session['user_id']
#         classes = Classes.query.filter_by(Instructor=instructor_id).all()
#         return render_template('teacher_classes.html', classes=classes)

# Route to display all courses
# Route to display all courses
@app.route('/all-courses', methods=['GET'])
def all_courses():
    # Query the database to get all course information
    courses = Classes.query.all()

    # Print the courses for debugging
    print(courses)

    # Create a list to store course data
    course_list = []

    # Iterate through the courses and append data to the list
    for course in courses:
        course_data = {
            'ClassId': course.ClassID,
            'ClassName': course.ClassName,
            'Instructor': course.Instructor,  # Assuming this is the instructor's name
            'MeetingTime': course.MeetingTime
        }
        course_list.append(course_data)

    # Print the course list for debugging
    print(course_list)

    # Render the HTML template and pass the course list
    return render_template('all_courses.html', courses=course_list)

@app.route('/show-all-courses')
def show_all_courses():
    courses = get_all_courses()
    return render_template('index.html', courses=courses)

@app.route('/stuCourses', methods=['GET'])
def stuCourses():
    requestStudent = request.get_json()
    user = Users.query.filter_by(name=requestStudent['name']).first() #This is assuming the user is signed in idk if this is the way to do this

    # After finding the user we use their ID to see ALL courses they are enrolled in
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'password': user.password,
            'type': user.type
            # Add other fields here
        }
        CourseRegistration.query.filter_by(student_id=user_data['id']).all()
        classListEnrolled = []
        classListEnrolled.append(user_data)
        return jsonify(classListEnrolled)
    else:
        return jsonify({'error': 'Invalid request'})

# @app.route('/schoolCourses', methods=['GET'])
# def schoolCourses():
#     # requestStudent = request.get_json()
#     # user = Users.query.filter_by(name=requestStudent['name']).first() #This is assuming the user is signed in idk if this is the way to do this

#     # After finding the user we use their ID to see ALL courses they are enrolled in
#     # if user:
#     #     user_data = {
#     #         'id': user.id,
#     #         'name': user.name,
#     #         'password': user.password,
#     #         'type': user.type
#     #         # Add other fields here
#     #     }
#         # Enrollment.query.filter_by(student_id=user_data['id']).all()
#         Class.query.all()
#         # classListEnrolled = []
#         # classListEnrolled.append(user_data)
#         return jsonify(Class.query.all())
#     # else:
#         # return jsonify({'error': 'Invalid request'})

@app.route('/signout', methods=['GET'])
def user_signout():
    # Clear session data
    session.clear()
    # Redirect the user to the sign-in page or homepage
    return redirect('/')  # Redirect to the sign-in page

@app.route('/user', methods=['POST'])
def create_student():
    if request.method == 'POST':
        requestStudent = request.get_json()
        newStudent = Users(FirstLastName=requestStudent['name'], Password=requestStudent['password'], Type=requestStudent['type'])
        db.session.add(newStudent)
        db.session.commit()
        # jsonify({'message': 'Student added'}), 200
        return jsonify({'message': 'Student created successfully'})
    else:
        return jsonify({'error': 'Invalid request'})
# @app.route('/grades/<name>', methods=['GET'])
@app.route('/userLogin', methods=['POST'])
def userLogin():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('name')  # Use the correct field name
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Please provide both username and password'}), 400

        user = Users.query.filter_by(FirstLastName=username).first()  # Use the correct field name
        if user:
            if user.Password == password:  # Use the correct field name
                return jsonify({'message': 'You have logged in'}), 200
            else:
                return jsonify({'error': 'Incorrect password'}), 401
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'Invalid request method'}), 405


@app.route('/allusers', methods=['GET'])
def allUsers():
    users = Users.query.all()
    classList = []

    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'password': user.password,
            'type': user.type
            # Add other fields here
        }
        classList.append(user_data)

    return jsonify(classList)



@app.route('/admin')
def admin():
    # Implement admin functionality here
    return render_template('admin.html')



@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    user = Users.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return redirect('/dashboard')  # Redirect to the user's dashboard
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('display_login'))




@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Check if a user with the same username already exists
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists. Please choose a different one.', 'error')
        return redirect(url_for('display_registration'))

    # Create a new user and add it to the database
    new_user = Users(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful. You can now log in.', 'success')
    return redirect(url_for('display_login'))

if __name__ == '__main__':
    app.run(debug=True)