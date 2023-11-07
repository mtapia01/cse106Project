from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'  # Use SQLite as an example database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Student, Teacher, Admin

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.relationship('User', backref='classes')
    max_capacity = db.Column(db.Integer)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    grade = db.Column(db.Float)

# Create the database tables
#db.create_all()


# Configure Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # The login route's name
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/register', methods=['GET'])
def display_registration():
    return render_template('registration.html')

#id = table organization Name = student/admin/teacher's name type = student/admin/teacher
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(7), nullable=False)

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
        Enrollment.query.filter_by(student_id=user_data['id']).all()
        classListEnrolled = []
        classListEnrolled.append(user_data)
        return jsonify(classListEnrolled)
    else:
        return jsonify({'error': 'Invalid request'})

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
        newStudent = Users(name=requestStudent['name'], password=requestStudent['password'], type=requestStudent['type'])
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
        username = data.get('username')  # Assuming the username is in the JSON data
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Please provide both username and password'}), 400

        user = Users.query.filter_by(name=username).first()
        if user:
            if user.password == password:  # Check if the passwords match
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
    user = User.query.filter_by(username=username, password=password).first()
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
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists. Please choose a different one.', 'error')
        return redirect(url_for('display_registration'))

    # Create a new user and add it to the database
    new_user = User(username=username, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful. You can now log in.', 'success')
    return redirect(url_for('display_login'))

