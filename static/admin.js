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

function forceEnrollStudent() {
    const studentId = $("#forceEnrollStudentForm input[name='user_id_to_force_enroll']").val();
    const newClassId = $("#forceEnrollStudentForm input[name='new_class_id_force_enroll']").val();

    const data = {
        student_id: studentId,
        new_class_id: newClassId
    };

    $.ajax({
        url: '/force_enroll_student',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
            alert(data.message);
            // Optionally, update the UI to reflect the enrollment
            // ...
        },
        error: function (error) {
            console.error('Error enrolling student:', error);
        }
    });

    return false; // Prevent form submission
}

function forceUnenrollStudentFromClass() {
    const studentId = $("#forceUnenrollStudentFromClassForm input[name='user_id_to_force_unenroll_class']").val();
    const classId = $("#forceUnenrollStudentFromClassForm input[name='class_id_to_unenroll_from']").val();

    const data = {
        student_id: studentId,
        class_id: classId
    };

    $.ajax({
        url: '/force_unenroll_student_from_class',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
            alert(data.message);
            // Optionally, update the UI to reflect the unenrollment from a specific class
            // ...
        },
        error: function (error) {
            console.error('Error unenrolling student from class:', error);
        }
    });

    return false; // Prevent form submission
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