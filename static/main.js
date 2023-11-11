var courseList;

function signout() {
    // Clear any stored authentication data (e.g., tokens, session data, cookies)
    // For instance, if using tokens:
    localStorage.removeItem('authToken'); // Remove token from local storage

    // Redirect the user to the sign-in page or homepage
    window.location.href = "/"; // Redirect to the sign-in page
}

function userLogin() {
    let studName = document.getElementById("stuName").value;
    const studPass = document.getElementById("stuPass").value;

    const data = { "name": studName, "password": studPass };

    const xmlhttp = new XMLHttpRequest();
    const method = 'POST'; // Considering this should be a POST request for login
    const url = 'http://127.0.0.1:5000/userLogin'; // Assuming this is the login endpoint

    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json"); // Setting the request header

    xmlhttp.onload = function () {
        if (xmlhttp.status === 200) {
            let loginDiv = document.getElementById("rcorners1");
            let loginBtn = document.getElementById("loginBtn");
            let signUpBtn = document.getElementById("signupBtn");
            let studentFunction = document.getElementById("postSignIn");
            loginDiv.classList.add("hide");
            loginBtn.classList.add("hide");
            signUpBtn.classList.add("hide");

            // Assuming you have a variable logOutBtn defined somewhere in your code
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

//might work need data to test
function openAllCourses() {
    document.getElementById("allCoursesModal").style.display = "block"; // Show the modal
    const resultDiv = document.getElementById("resultAllCourses");

    // API request
    const xmlhttp = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://127.0.0.1:5000/all-courses';  // Correct endpoint

    xmlhttp.open(method, url, true);
    xmlhttp.send();

    xmlhttp.onload = function () {
        if (xmlhttp.status === 200) {
            const classList = JSON.parse(xmlhttp.response);
            // Rest of your code
        } else {
            console.error("Failed to fetch courses:", xmlhttp.statusText);
            alert("Failed to fetch courses. Please try again later.");
        }
    };

    // Handle network errors
    xmlhttp.onerror = function () {
        console.error("Network error occurred.");
        alert("Failed to fetch courses due to a network error.");
    };
}



function registerForClass(classID, button) {
    const username = document.getElementById("stuName").value;

    const xmlhttp = new XMLHttpRequest();
    const method = 'POST';
    const url = 'http://127.0.0.1:5000/registerClass';

    const data = {
        user_id: username,
        class_id: classID
    };

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            const response = JSON.parse(xmlhttp.responseText);
            if (response.status === 'registered') {
                button.innerHTML = 'DeRegister';
            } else if (response.status === 'deregistered') {
                button.innerHTML = 'Register';
            }
            
            // Disable the button if the user is registered
            button.disabled = response.status === 'registered';
            // Add a CSS class to visually indicate that the button is disabled
            button.classList.toggle('disabled', response.status === 'registered');
        }
    };

    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    xmlhttp.send(JSON.stringify(data));
}


function openMyCourses() {
    document.getElementById("myModal").style.display = "block"; // Show the modal
    const resultDiv = document.getElementById("resultAll");
    const xmlhttp = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://127.0.0.1:5000/stuCourses';

    let studName = document.getElementById("stuName").value;
    const data = { "name": studName };

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            // Parse the JSON response
            courseList = JSON.parse(xmlhttp.responseText);

            // Create an HTML table
            let tableHTML = '<table border="1">';
            tableHTML += '<tr><th>Name</th><th>Grade</th><th>Action</th></tr>';

            for (let i = 0; i < courseList.length; i++) {
                let courseName = courseList[i].course_name;
                let grade = courseList[i].grade;
                let classId = courseList[i].class_id;

                // Creating table rows with a deregister button
                tableHTML += `<tr><td>${courseName}</td><td>${grade}</td><td><button onclick="deregisterCourse(${i}, ${classId})">Deregister</button></td></tr>`;
            }
            tableHTML += '</table>';
            resultDiv.innerHTML = tableHTML;
        }
    };

    xmlhttp.open(method, `${url}?name=${studName}`, true);  // Pass the name as a query parameter
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(JSON.stringify(data));
}

function deregisterCourse(index) {
    const xmlhttp = new XMLHttpRequest();
    const method = 'POST';
    const url = 'http://127.0.0.1:5000/deregisterCourse';

    const classId = courseList[index].class_id; 
    let studName = document.getElementById("stuName").value;
    const data = JSON.stringify({ "name": studName, "class_id": classId });

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            // Refresh the table after deregistering
            openMyCourses();
        }
    };

    xmlhttp.open(method, url, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(data);
}


function closeMyCourses() {
    // Hide the modals
    document.getElementById("myModal").style.display = "none"; 
    document.getElementById("allCoursesModal").style.display = "none";
    document.getElementById("registerCoursesModal").style.display = "none";
}

function closeAllCourses() {
    document.getElementById("myModal").style.display = "none"; // Hide the modal
}

function postStudent() {
    const name = document.getElementById("stuName").value;
    const pass = document.getElementById("stuPass").value;
    const type = "student";

    const data = { name: name, password: pass, type: type };

    fetch('http://127.0.0.1:5000/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (response.ok) {
                // Show a success message in a modal or an alert
                alert("Registration successful! You can now log in.");
                // Redirect the user to the login page
                window.location.href = "/";
            } else {
                // Show an error message if registration fails
                alert("Registration failed. Please try again.");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Show an error message if there is an issue with the request
            alert("There was an error during the registration process.");
        });

        const responseData = await response.json();

        // Show an alert with the error message, or "Success" if there's no error
        alert(responseData.error || 'Success');

        console.log(responseData);
    } catch (error) {
        console.error('Error:', error);
    }
}
function teacherLogin(){}
function postTeacher(){}