// Wait for the document to be ready before executing the script
$(document).ready(function () {
    // Fetch teachers and populate the dropdown
    fetchTeachers();
    fetchStudents();

    // Submit form handler
    $('#createClassForm').submit(function (event) {
        event.preventDefault(); // Prevent the default form submission
        // Add your form submission logic here, if needed
    });
});

function fetchTeachers() {
    $.ajax({
        url: '/get_teachers',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            const uniqueTeachers = Array.from(new Set(data.map(teacher => teacher.UserId)));

            populateTeacherDropdown(data.filter(teacher => uniqueTeachers.includes(teacher.UserId)));
        },
        error: function (error) {
            console.error('Error fetching teachers:', error);
        }
    });
}

function populateTeacherDropdown(teachers) {
    const teacherDropdown = $('#teacherDropdown');
    teacherDropdown.empty(); // Clear the dropdown before populating

    const uniqueTeachers = Array.from(new Set(teachers.map(teacher => teacher.UserId)));

    uniqueTeachers.forEach(function (userId) {
        const teacher = teachers.find(t => t.UserId === userId);
        const option = $('<option>').val(teacher.UserId).text(teacher.FirstLastName);
        teacherDropdown.append(option);
    });
}

function createClass() {
    const className = $("#createClassForm input[name='class_name']").val();
    const teacherId = $("#createClassForm select[name='teacher_id']").val();
    const maxCapacity = $("#createClassForm input[name='max_capacity']").val();
    const classId = $("#createClassForm input[name='class_id']").val();
    const meetingTime = $("#createClassForm input[name='meetingTime']").val();



    const formData = {
        class_id: classId,
        class_name: className,
        teacher_id: teacherId,
        max_capacity: maxCapacity,
        meetingTime: meetingTime
    };

    const xhr = new XMLHttpRequest();
    const url = '/create_class';

    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Request was successful
                alert('Class created successfully');
            } else {
                // Request failed
                alert('Error creating class. Please try again.');
            }
        }
    };

    // Convert the form data to JSON format
    const jsonData = JSON.stringify(formData);

    // Send the request
    xhr.send(jsonData);
}


// Wait for the document to be ready before executing the script
$(document).ready(function () {
    
    // Submit delete class form handler
    $('#deleteClassForm').submit(function (event) {
        event.preventDefault(); // Prevent the default form submission
        const classIdToDelete = $("#deleteClassForm input[name='class_id_to_delete']").val();
        deleteClass(classIdToDelete);
    });
});

// Function to delete a class
function deleteClass(classId) {
    const url = `/delete_class/${classId}`;

    $.ajax({
        url: url,
        method: 'POST',
        success: function (data) {
            alert(data.message);
        },
        error: function (error) {
            console.error('Error deleting class:', error);
        }
    });
}

function getStudentsInClass() {
    let classID = document.getElementById("classID").value;
    // alert(classID)
    const url = `/get_students_in_class/${classID}`;

    $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            // Populate the table with the class information
            $('#studentTable tbody').append(`
                <tr>
                    <td>${classID}</td>
                   
                </tr>
            `);

            // Populate the table with the retrieved student data
            data.students.forEach(function (student) {
                $('#studentTable tbody').append(`
                    <tr>
                        <td></td> <!-- Empty cell for alignment -->
                        <td>${student.UserId}</td>
                        <td>${student.FirstLastName}</td>
                    </tr>
                `);
            });
        },
        error: function (error) {
            console.error('Error fetching students in class:', error);
        }
    });
}



// Function to change user credentials
function changeUserCredentials() {
    const userIdToChange = $("#changeUserCredentialsForm input[name='user_id_to_change']").val();
    const newUsername = $("#changeUserCredentialsForm input[name='new_username']").val();
    const newPassword = $("#changeUserCredentialsForm input[name='new_password']").val();

    const url = `/change_user_credentials/${userIdToChange}`;

    const data = {
        new_username: newUsername, 
        new_password: newPassword
    };

    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
            alert(data.message);
        },
        error: function (error) {
            console.error('Error changing user credentials:', error);
        }
    });

    return false; // Prevent the form from submitting
}

function createUser() {
    const newUsername = $("#createUserForm input[name='new_username']").val();
    const newPassword = $("#createUserForm input[name='new_password']").val();
    const userType = $("#createUserForm input[name='user_type']").val();

    const formData = {
        new_username: newUsername,
        new_password: newPassword,
        user_type: userType
    };

    $.ajax({
        url: '/create_user',
        method: 'POST',
        data: JSON.stringify(formData),
        contentType: 'application/json',
        success: function (data) {
            alert(data.message);
        },
        error: function (error) {
            console.error('Error creating user:', error);
        }
    });

    // Prevent the default form submission
    return false;
}

// Add this function to admin.js
function forceStudentsIntoClass() {
    const classID = document.getElementsByName("class_id_to_force_students")[0].value;
    const studentID = document.getElementById("studentDropdown").value;

    const xmlhttp = new XMLHttpRequest();
    const method = 'POST';
    const url = 'http://127.0.0.1:5000/forceStudentsIntoClass';

    const data = {
        class_id: classID,
        student_id: studentID
    };

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            const response = JSON.parse(xmlhttp.responseText);
            document.getElementById("resultForceStudentsIntoClass").innerHTML = response.message;
        }
    };

    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xmlhttp.send(JSON.stringify(data));
    return false; // Prevent the form from submitting normally
}

// Add this function to fetch students
function fetchStudents() {
    $.ajax({
        url: '/get_students',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            populateStudentDropdown(data);
        },
        error: function (error) {
            console.error('Error fetching students:', error);
        }
    });
}

// Add this function to populate the student dropdown
function populateStudentDropdown(students) {
    const studentDropdown = $('#studentDropdown');
    studentDropdown.empty(); // Clear the dropdown before populating

    const uniqueStudents = Array.from(new Set(students.map(student => student.UserId)));

    uniqueStudents.forEach(function (userId) {
        const student = students.find(s => s.UserId === userId);
        const option = $('<option>').val(student.UserId).text(student.FirstLastName);
        studentDropdown.append(option);
    });
}