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
        tableHTML += '<tr><th>Name</th><th>Grade</th></tr>';

        const classList = JSON.parse(xmlhttp.response);

        for (let i = 0; i < classList.length; i++) {
            let person = classList[i].key;
            let grade = classList[i].value;

            // Creating table rows
            tableHTML += `<tr><td>${person}</td><td>${grade}</td></tr>`;
        }
        tableHTML += '</table>';
        resultDiv.innerHTML = tableHTML;
    }
}

function closeMyCourses() {
    document.getElementById("myModal").style.display = "none"; // Hide the modal
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
}
function teacherLogin(){}
function postTeacher(){}