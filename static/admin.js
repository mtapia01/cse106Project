// Wait for the document to be ready before executing the script
$(document).ready(function () {
    // Fetch teachers and populate the dropdown
    fetchTeachers();

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
            populateTeacherDropdown(data);
        },
        error: function (error) {
            console.error('Error fetching teachers:', error);
        }
    });
}

function populateTeacherDropdown(teachers) {
    const teacherDropdown = $('#teacherDropdown');
    teachers.forEach(function (teacher) {
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
    // Other initialization code...

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
            // Optionally, update the UI to reflect the deleted class
            // ...
        },
        error: function (error) {
            console.error('Error deleting class:', error);
        }
    });
}

function getStudentsInClass(ClassId) {
    const url = `/get_students_in_class/${ClassId}`;

    $.ajax({
        url: url,
        method: 'GET',
        success: function (data) {
            // Handle the retrieved student data, e.g., display in a modal
            // ...
        },
        error: function (error) {
            console.error('Error fetching students in class:', error);
        }
    });
}

function changeStudentClass(studentId, newClassId) {
    const url = `/change_student_class/${studentId}`;

    const data = {
        new_class_id: newClassId
    };

    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
            alert(data.message);
            // Optionally, update the UI to reflect the changed class
            // ...
        },
        error: function (error) {
            console.error('Error changing student class:', error);
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
        new_username: newUsername,  // Assuming newUsername contains the new username
        new_password: newPassword
    };

    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
            alert(data.message);
            // Optionally, update the UI to reflect the changed credentials
            // ...
        },
        error: function (error) {
            console.error('Error changing user credentials:', error);
        }
    });

    return false; // Prevent the form from submitting
}