from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
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
    HashedPasswords = db.Column(db.String(80))

    def to_dict(self):
        return {
            'ClassID': self.FirstLastName,
        }

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
    


# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # The login route's name
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



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
    return render_template('student.html')

    
@app.route('/teacher')
def teacher():
        instructor_id = session.get('username')
        teacher_classes = Classes.query.filter_by(Instructor=instructor_id).all()
        return render_template('teacher.html', teacher_classes=teacher_classes)


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

@app.route('/get_students', methods=['GET'])
def get_students():
    students = Users.query.filter_by(Type=1).all()
    students_data = [{'UserId': student.UserId, 'FirstLastName': student.FirstLastName} for student in students]
    sorted_students_data = sorted(students_data, key=lambda x: x['FirstLastName'])
    return jsonify(sorted_students_data)

@app.route('/teacher/manage_grades/<int:class_id>', methods=['GET', 'POST'])
def manage_grades(class_id):
    if request.method == 'GET':
        # Fetch the class details and enrolled students for the given class_id
        target_class = Classes.query.get(class_id)

        if target_class:
            enrolled_students = CourseRegistration.query.filter_by(ClassIDFK=class_id).all()
            
            # Fetch user information for each student
            students_info = []
            for student in enrolled_students:
                user = Users.query.get(student.UserIdFK)
                students_info.append({
                    'UserIdFK': student.UserIdFK,
                    'FirstLastName': user.FirstLastName,
                    'Grade': student.Grade
                })

            return render_template('manage_grades.html', target_class=target_class, enrolled_students=students_info)
        else:
            flash('Class not found', 'error')
            return redirect('/teacher')  # Redirect to teacher page or handle accordingly
    
    elif request.method == 'POST':
        # Handle form submission to update grades
        data = request.form
        for student_id, grade in data.items():
            registration = CourseRegistration.query.filter_by(UserIdFK=student_id, ClassIDFK=class_id).first()
            if registration:
                registration.Grade = grade
                db.session.commit()

        flash('Grades updated successfully', 'success')
        return redirect(url_for('manage_grades', class_id=class_id))


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

    return jsonify({"error": "Invalid request method"}), 405

@app.route('/delete_class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    # Check if the class exists
    course = Classes.query.get(class_id)
    if not course:
        return jsonify({'message': 'Class not found'}), 404

    # Delete the class
    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Class deleted successfully'}), 200


@app.route('/get_students_in_class/<int:class_id>', methods=['GET'])
def get_students_in_class(class_id):
    try:
        # Query the registrations for the given class_id
        registrations = CourseRegistration.query.filter_by(ClassIDFK=class_id).all()

        # Extract user IDs from registrations
        user_ids = [registration.UserIdFK for registration in registrations]

        # Query user details for the extracted user IDs
        students = Users.query.filter(Users.UserId.in_(user_ids)).all()

        # Prepare the response data
        student_data = [{'UserId': student.UserId, 'FirstLastName': student.FirstLastName} for student in students]

        return jsonify({'students': student_data}), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching students: {str(e)}'}), 500


@app.route('/change_user_credentials/<int:user_id>', methods=['POST'])
def change_user_credentials(user_id):
    try:
        # Get the data from the request
        data = request.get_json()

        # Extract data from the request
        new_username = data.get('new_username')
        new_password = data.get('new_password')

        # Query the user to update
        user = Users.query.get(user_id)

        if user:
            # Update the username and/or password
            if new_username:
                user.FirstLastName = new_username
            if new_password:
                # Hash the new password before updating
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.HashedPasswords = hashed_password
                user.Password = new_password

            db.session.commit()

            return jsonify({'message': 'User credentials updated successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        # Handle exceptions and log errors if needed
        return jsonify({'message': f'Error changing user credentials: {str(e)}'}), 500
    

@app.route('/signout', methods=['GET'])
def user_signout():
    # Clear session data
    session.clear()
    # Redirect the user to the sign-in page or homepage
    return redirect('/')  # Redirect to the sign-in page


@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        username = data.get('new_username')
        password = data.get('new_password')
        user_type = data.get('user_type')

        # Check if the username already exists
        existing_user = Users.query.filter_by(FirstLastName=username).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        # Create a new user
        new_user = Users(FirstLastName=username, Password=password, Type=user_type)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        app.logger.error(f"Error creating user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/userLogin', methods=['POST'])
def userLogin():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('name')
        password = data.get('password')
        session['username'] = username

        if not username or not password:
            return jsonify({'error': 'Please provide both username and password'}), 400

        user = Users.query.filter_by(FirstLastName=username).first()

        if user:
            if bcrypt.check_password_hash(user.HashedPasswords, password):
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
    # Fetch all users from the Users table
    all_users = Users.query.all()
    return render_template('admin.html', all_users=all_users)

bcrypt = Bcrypt(app)

@app.route('/user', methods=['POST'])
def create_student():
    if request.method == 'POST':
        requestStudent = request.get_json()

        registration = Users.query.filter_by(FirstLastName=requestStudent['username']).first()

        if registration:
            return jsonify({'error': 'User Already Exists'})
        else:
            hashed_password = bcrypt.generate_password_hash(requestStudent['password']).decode('utf-8')
            newStudent = Users(FirstLastName=requestStudent['username'], Password=hashed_password, Type=requestStudent['type'])
            db.session.add(newStudent)
            db.session.commit()
            return jsonify({'message': 'Student created successfully'})
    else:
        return jsonify({'error': 'Invalid request'})

@app.route('/forceStudentsIntoClass', methods=['POST'])
def force_students_into_class():
    if request.method == 'POST':
        data = request.get_json()
        class_id = data.get('class_id')
        student_id = data.get('student_id')

        # Check if the user is of type 1 (student)
        student = Users.query.filter_by(UserId=student_id, Type=1).first()

        if not student:
            return jsonify({'status': 'error', 'message': 'Invalid student ID or not a student.'})

        # Check if the class exists
        target_class = Classes.query.get(class_id)

        if not target_class:
            return jsonify({'status': 'error', 'message': 'Invalid class ID.'})

        # Check if the student is already enrolled in the class
        existing_registration = CourseRegistration.query.filter_by(UserIdFK=student_id, ClassIDFK=class_id).first()

        if existing_registration:
            return jsonify({'status': 'error', 'message': 'Student is already enrolled in the class.'})
        else:
            # Create a new registration
            new_registration = CourseRegistration(UserIdFK=student_id, ClassIDFK=class_id, Grade=100)
            db.session.add(new_registration)

            # Increment the EnrolledStudents count in the Classes table
            target_class.EnrolledStudents += 1

            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Student forced into class.'})

if __name__ == '__main__':
    app.run(debug=True)
