from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'dbs', 'users.db')
db = SQLAlchemy(app)

app.secret_key = 'key'

class Users(db.Model, UserMixin):
    UserId = db.Column(db.Integer, primary_key=True)
    FirstLastName = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(120), nullable=False)
    Type = db.Column(db.Integer, nullable=False, default=1)  # Student, Teacher, Admin

class Classes(db.Model):
    ClassID = db.Column(db.Integer, primary_key=True)
    ClassName = db.Column(db.String(80), nullable=False)
    Instructor = db.Column(db.Integer, db.ForeignKey('users.FirstLastName'))
    MeetingTime = db.Column(db.String(80), nullable=True)
    EnrolledStudents = db.Column(db.Integer)
    MaxStudents = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'ClassID': self.ClassID,
            'ClassName': self.ClassName,
            'Instructor': self.Instructor,
            'MeetingTime': self.MeetingTime,
            'EnrolledStudents': self.EnrolledStudents,
            'MaxStudents': self.MaxStudents
        }

class CourseRegistration(db.Model):
    __tablename__ = 'CourseRegistration'  # Specify the correct table name
    UserIdFK = db.Column(db.Integer, db.ForeignKey('users.UserId'))
    ClassIDFK = db.Column(db.Integer, db.ForeignKey('classes.ClassID'))
    Grade = db.Column(db.Float, nullable=True)
    RegistrationID = db.Column(db.Integer, primary_key=True)
    

# Create the database tables
#db.create_all()


# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # The login route's name
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

def create_admin_user():
    admin_exists = User.query.filter_by(type='admin').first()

    if not admin_exists:
        # If admin user doesn't exist, create one
        admin_user = User(name='admin', password='admin1', type='admin')
        db.session.add(admin_user)
        db.session.commit()
        print('Admin user created successfully.')

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
@login_required
def teacher():
    # Assuming you have a function to fetch classes for the logged-in teacher
    classes = get_teacher_classes(current_user.id)

    # Assuming you have a function to fetch grades for the logged-in teacher
    grades = get_teacher_grades(current_user.id)

    return render_template('teacher.html', classes=classes, grades=grades)

def get_teacher_classes(user_id):
    # Assuming you have a User model with a relationship to classes
    # and the Instructor field in the Classes model corresponds to the teacher's user ID
    return Classes.query.filter_by(Instructor=user_id).all()

def get_teacher_grades(user_id):
    # Assuming you have a function to fetch grades for the logged-in teacher
    # This could involve querying the CourseRegistration table and joining with other necessary tables
    # Adjust the query based on your database schema
    # The assumption is that the CourseRegistration table has a relationship with the User and Classes models
    # to get the student name and class name
    return CourseRegistration.query\
        .join(Users, CourseRegistration.UserIdFK == Users.UserId)\
        .join(Classes, CourseRegistration.ClassIDFK == Classes.ClassID)\
        .filter(Classes.Instructor == user_id)\
        .all()
        
# @app.route('/teacher/classes')
# def teacher_classes():
#     if 'user_id' in session and session['user_type'] == 2:  # Ensure the user is a teacher (user type 2)
#         instructor_id = session['user_id']
#         classes = Classes.query.filter_by(Instructor=instructor_id).all()
#         return render_template('teacher_classes.html', classes=classes)

@app.route('/stuCourses', methods=['GET'])
def stuCourses():
    username = request.args.get('name')
    
    # After finding the user, use their ID to fetch ALL courses they are enrolled in
    user = Users.query.filter_by(FirstLastName=username).first()

    if user:
        # Fetch the courses enrolled by the user
        enrolled_courses = CourseRegistration.query.filter_by(UserIdFK=user.UserId).all()

        # Create a list to store the courses
        classListEnrolled = []

        # Iterate through the enrolled courses and add course information to the list
        for enrollment in enrolled_courses:
            # Use the correct attribute from the CourseRegistration model
            class_id = enrollment.ClassIDFK

            course = Classes.query.filter_by(ClassID=class_id).first()

            if course:
                classListEnrolled.append({
                    'course_name': course.ClassName,
                    'grade': enrollment.Grade,
                    'class_id': class_id  # Add the class_id to the response
                })
            else:
                # Handle the case where the course information is not found
                classListEnrolled.append({
                    'error': 'Course information not found',
                    'grade': enrollment.Grade,
                    'class_id': class_id  # Add the class_id to the response even if not found
                })

        return jsonify(classListEnrolled)
    else:
        return jsonify({'error': 'Invalid user'})


@app.route('/schoolCourses', methods=['GET'])
def schoolCourses():
    if request.method == 'GET':
        classes = Classes.query.all()
        classes_list = [cls.to_dict() for cls in classes]
        return jsonify(classes_list)
    
@app.route('/registerClass', methods=['POST'])
def courseRegister():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('user_id')

        user_id = Users.query.filter_by(FirstLastName=username).first().UserId
        class_id = data.get('class_id')  # Assuming 'class_id' is sent in the JSON payload

        # Check if the user is already registered for the class
        existing_registration = CourseRegistration.query.filter_by(UserIdFK=user_id, ClassIDFK=class_id).first()

        if existing_registration:
            # If the user is already registered, remove the registration (deregister)
            db.session.delete(existing_registration)

            # Decrement the EnrolledStudents count in the Classes table
            target_class = Classes.query.get(class_id)
            if target_class and target_class.EnrolledStudents > 0:
                target_class.EnrolledStudents -= 1

            db.session.commit()
            return jsonify({'status': 'deregistered'})
        else:
            # If the user is not registered, create a new registration
            new_registration = CourseRegistration(UserIdFK=user_id, ClassIDFK=class_id, Grade=100)
            db.session.add(new_registration)

            # Increment the EnrolledStudents count in the Classes table
            target_class = Classes.query.get(class_id)
            if target_class:
                target_class.EnrolledStudents += 1

            db.session.commit()
            return jsonify({'status': 'registered'})

@app.route('/deregisterCourse', methods=['POST'])
def deregisterCourse():
    data = request.get_json()
    class_id = data.get('class_id')
    name = data.get('name')
    

    user = Users.query.filter_by(FirstLastName=name).first()
    if user:
        registration = CourseRegistration.query.filter_by(UserIdFK=user.UserId, ClassIDFK=class_id).first()
        if registration:
            target_class = Classes.query.get(class_id)
            if target_class and target_class.EnrolledStudents > 0:
                target_class.EnrolledStudents -= 1

            db.session.delete(registration)
            db.session.commit()
            return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error'})

@app.route('/get_teachers', methods=['GET'])
def get_teachers():
    teachers = Users.query.filter_by(Type=2).all()
    teachers_data = [{'UserId': teacher.UserId, 'FirstLastName': teacher.FirstLastName} for teacher in teachers]
    sorted_teachers_data = sorted(teachers_data, key=lambda x: x['FirstLastName'])
    return jsonify(sorted_teachers_data)


# @app.route('/createClass', methods=['GET'])
# def show_create_class_form():
#     teachers = Users.query.filter_by(Type=2).all()
#     return render_template('create_class.html', teachers=teachers)

@app.route('/create_class', methods=['POST'])
def create_class():
    if request.method == 'POST':
        data = request.get_json()

        class_id = data.get('class_id')
        class_name = data.get('class_name')
        teacher_id = data.get('teacher_id')
        max_capacity = data.get('max_capacity')
        meetingTime = data.get('meetingTime')
        
        instructor = Users.query.filter_by(UserId=teacher_id).first().FirstLastName


        # Validate the input data (you might want to add more validation)
        if not class_name or not teacher_id or not max_capacity:
            return jsonify({"error": "Invalid form data. Please fill in all fields"}), 400

        # Create a new class
        new_class = Classes(
            ClassID = class_id,
            ClassName=class_name,
            Instructor=instructor,
            MaxStudents=max_capacity,
            MeetingTime=meetingTime,
            EnrolledStudents=0  # Initially, no students are enrolled
        )

        db.session.add(new_class)
        db.session.commit()

        return jsonify({"message": "Class created successfully"}), 200

    # If the request is not a POST request, you might want to handle it accordingly
    return jsonify({"error": "Invalid request method"}), 405

    

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
        
        registration = Users.query.filter_by(FirstLastName=requestStudent['username']).first()

        if registration:
            return jsonify({'error': 'User Already Exists'})
        else:
            newStudent = Users(FirstLastName=requestStudent['username'], Password=requestStudent['password'], Type=requestStudent['type'])
            db.session.add(newStudent)
            db.session.commit()
            return jsonify({'message': 'Student created successfully'})
    else:
        return jsonify({'error': 'Invalid request'})
    
# @app.route('/grades/<name>', methods=['GET'])
@app.route('/userLogin', methods=['POST'])
def userLogin():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('name')
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


@app.route('/getType', methods=['POST'])
def getType():
    data = request.get_json()
    username = data.get('userName')
    uType = Users.query.filter_by(FirstLastName=username).first().Type
    return jsonify(uType)


@app.route('/admin')
def admin():
    # Implement admin functionality here
    return render_template('admin.html')



@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = Users.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return redirect('/dashboard')  # Redirect to the user's dashboard
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('display_login'))

if __name__ == '__main__':
    app.run(debug=True)


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