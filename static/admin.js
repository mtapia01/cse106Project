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

function getStudentsInClass(classId) {
    const url = `/get_students_in_class/${classId}`;

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

function changeUserCredentials(userId, newUsername, newPassword) {
    const url = `/change_user_credentials/${userId}`;

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
            // Optionally, update the UI to reflect the changed credentials
            // ...
        },
        error: function (error) {
            console.error('Error changing user credentials:', error);
        }
    });
}
