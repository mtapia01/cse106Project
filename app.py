from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use SQLite as an example database
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


@app.route('/', methods=['GET'])
def display_login():
    return render_template('login.html')

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

@app.route('/teacher/classes')
def teacher_classes():
    if 'user_id' in session and session['user_type'] == 2:  # Ensure the user is a teacher (user type 2)
        instructor_id = session['user_id']
        classes = Classes.query.filter_by(Instructor=instructor_id).all()
        return render_template('teacher_classes.html', classes=classes)



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

