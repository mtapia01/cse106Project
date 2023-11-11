function signout() {
    // Clear any stored authentication data (e.g., tokens, session data, cookies)
    // For instance, if using tokens:
    localStorage.removeItem('authToken'); // Remove token from local storage

    // Redirect the user to the sign-in page or homepage
    window.location.href = "/"; // Redirect to the sign-in page
}
var data = { "name": studName, "password": studPass };

function userLogin() {
    let studName = document.getElementById("stuName").value;
    const studPass = document.getElementById("stuPass").value;

    data = { "name": studName, "password": studPass };

    const xmlhttp = new XMLHttpRequest();
    const method = 'POST'; 
    const url = 'http://127.0.0.1:5000/userLogin'; 

    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json"); 

    xmlhttp.onload = function () {
        if (xmlhttp.status === 200) {
            let loginDiv = document.getElementById("rcorners1");
            let loginBtn = document.getElementById("loginBtn");
            let signUpBtn = document.getElementById("signupBtn");
            let studentFunction = document.getElementById("postSignIn");
            loginDiv.classList.add("hide");
            loginBtn.classList.add("hide");
            signUpBtn.classList.add("hide");

            
            logOutBtn.classList.remove("hide");
            logOutBtn.classList.add("button");
            logOutBtn.classList.add("button1");

            studentFunction.classList.remove("hide");
        } else {
            alert("Login failed. Please check your credentials.");
        }
    };

    xmlhttp.onerror = function () {
        alert("There was an error during the login process.");
    };
    xmlhttp.send(JSON.stringify(data));
}

function registerCourses(){
    document.getElementById("openCourses").style.display = "block"; // Show the modal
    const resultDiv = document.getElementById("resultRegister");
    const xmlhttp = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://127.0.0.1:5000/schoolCourses ';
    xmlhttp.open(method, url, true);
    xmlhttp.send();
    xmlhttp.onload = function () {

        // Create an HTML table
        let tableHTML = '<table border="1">';
        tableHTML += '<tr><th>Course</th><th>Instructor</th><th>Meeting Time</th><th>Enrolled Students</th><th>Max Students</th><th>Action</th></tr>';

        classList = JSON.parse(xmlhttp.response);

        for (let i = 0; i < classList.length; i++) {
            let course = classList[i].ClassName;
            let instructor = classList[i].Instructor;
            let meetingTime = classList[i].MeetingTime;
            let enrolledStudents = classList[i].EnrolledStudents;
            let maxStudents = classList[i].MaxStudents;

            // Creating table rows with a button for each course
            tableHTML += `<tr><td>${course}</td><td>${instructor}</td><td>${meetingTime}</td><td>${enrolledStudents}</td><td>${maxStudents}</td><td><button onclick="addCourse('${course}')">Add</button></td></tr>`;
        }
        tableHTML += '</table>';
        resultDiv.innerHTML = tableHTML;
    }
}

function addCourse(courseName) {
    const xmlhttp = new XMLHttpRequest();

    const url = 'http://127.0.0.1:5000/addCourse'; 
    const data = { course: courseName };

    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader('Content-Type', 'application/json');
    xmlhttp.send(JSON.stringify(data));

    xmlhttp.onload = function () {
        if (xmlhttp.status === 200) {
            alert(`Course ${courseName} added successfully!`);
        } else {
            alert(`Failed to add course ${courseName}.`);
        }
    };
}

//might work need data to test
function openAllCourses(){
    document.getElementById("allCoursesModal").style.display = "block"; // Show the modal
    const resultDiv = document.getElementById("resultAllCourses");
    const xmlhttp = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://127.0.0.1:5000/schoolCourses ';
    xmlhttp.open(method, url, true);
    xmlhttp.send();
    xmlhttp.onload = function () {

        // Create an HTML table
        let tableHTML = '<table border="1">';
        tableHTML += '<tr><th>Course</th><th>Instructor</th><th>Meeting Time</th><th>Enrolled Students</th><th>Max Students</th></tr>';

        classList = JSON.parse(xmlhttp.response);

        for (let i = 0; i < classList.length; i++) {
            let course = classList[i].ClassName;
            let instructor = classList[i].Instructor;
            let meetingTime = classList[i].MeetingTime;
            let enrolledStudents = classList[i].EnrolledStudents;
            let maxStudents = classList[i].MaxStudents;

            // Creating table rows
            tableHTML += `<tr><td>${course}</td><td>${instructor}</td><td>${meetingTime}</td><td>${enrolledStudents}</td><td>${maxStudents}</td></tr>`;
        }
        tableHTML += '</table>';
        resultDiv.innerHTML = tableHTML;
    }
}

function openMyCourses(){
    document.getElementById("myModal").style.display = "block"; // Show the modal
    const resultDiv = document.getElementById("resultAll");
    const xmlhttp = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://127.0.0.1:5000/stuCourses';
    xmlhttp.open(method, url, true);
    xmlhttp.send();
    xmlhttp.onload = function () {

        // Create an HTML table
        let tableHTML = '<table border="1">';
        tableHTML += '<tr><th>Course</th><th>Instructor</th><th>Meeting Time</th><th>Enrolled Students</th><th>Max Students</th></tr>';

        classList = JSON.parse(xmlhttp.response);

        for (let i = 0; i < classList.length; i++) {
            let course = classList[i].ClassName;
            let instructor = classList[i].Instructor;
            let meetingTime = classList[i].MeetingTime;
            let enrolledStudents = classList[i].EnrolledStudents;
            let maxStudents = classList[i].MaxStudents;

            // Creating table rows
            tableHTML += `<tr><td>${course}</td><td>${instructor}</td><td>${meetingTime}</td><td>${enrolledStudents}</td><td>${maxStudents}</td></tr>`;
        }
        tableHTML += '</table>';
        resultDiv.innerHTML = tableHTML;
    }
}

function closeMyCourses() {
    document.getElementById("myModal").style.display = "none"; // Hide the modal
}

function closeAllCourses() {
    document.getElementById("allCoursesModal").style.display = "none"; // Hide the modal
}
function closeRegister() {
    document.getElementById("openCourses").style.display = "none"; // Hide the modal
}

async function postStudent() {
    const username = document.getElementById("stuName").value;
    const pass = document.getElementById("stuPass").value;
    const type = 1;

    const data = { username: username, password: pass, type: type };

    fetch('http://127.0.0.1:5000/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function teacherLogin(){}
function postTeacher(){}