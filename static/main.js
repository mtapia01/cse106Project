// function userLogin(){
//     let studName = document.getElementById("stuName").value;
//     const studPass = document.getElementById("stuPass").value;

//     const xmlhttp = new XMLHttpRequest();
//     const method = 'GET';
//     const url = 'http://127.0.0.1:5000/userLogin/${studName}${studPass}';

//     xmlhttp.open(method, url, true);
//     xmlhttp.send();
//     xmlhttp.onload = function () {
//         let loginDiv = document.getElementById("rcorners1");
//         let loginBtn = document.getElementById("loginBtn");
//         let signUpBtn = document.getElementById("signupBtn");
//         if(response.ok){
//             loginDiv.classList.add("hide");
//             loginDiv.classList.add("hide");
//             signUpBtn.classList.add("hide");
//             loginBtn.classList.add("hide")
//         } else{
//             console.log(response.json())
//             // console.error('Error:', error);
//             alert(error)
//         }
//     };
// }

function signout(){

    // Clear any stored authentication data (e.g., tokens, session data, cookies)
    // For instance, if using tokens:
    localStorage.removeItem('authToken'); // Remove token from local storage

    // Redirect the user to the sign-in page or homepage
    window.location.href = "/"; // Redirect to the sign-in page

}

function userLogin() {
    let studName = document.getElementById("stuName").value;
    const studPass = document.getElementById("stuPass").value;

    const data = {"username": studName, "password": studPass};

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
            loginDiv.classList.add("hide");
            loginBtn.classList.add("hide");
            signUpBtn.classList.add("hide");
            logOutBtn.classList.remove("hide");
            logOutBtn.classList.add("button");
            logOutBtn.classList.add("button1");
        } else {
            alert("Login failed. Please check your credentials.");
        }
    };

    xmlhttp.onerror = function() {
        alert("There was an error during the login process.");
    };

    // Prepare and send the request
    // const data = JSON.stringify({ "name": studName, "password": studPass });
    // xmlhttp.send(data);
    xmlhttp.send(JSON.stringify(data));
}

async function postStudent(){
    const name = document.getElementById("stuName").value;
    const pass = document.getElementById("stuPass").value;
    const type = "student"

    const data = {name: name, password: pass, type: type};

    fetch('http://127.0.0.1:5000/user', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
    })
    .then((response) => {
        console.log(response);
        // console.log('Success:', response.json());
        console.log(response.json())
        // const resultDiv = document.getElementById("postResult");
        // resultDiv.innerHTML = `Successfully added ${name} to the table!`;
    })
    .catch((error) => {
        console.error('Error:', error);
        // const resultDiv = document.getElementById("postResult");
        // resultDiv.innerHTML = `Could not add ${name} to the table`;
    });
}