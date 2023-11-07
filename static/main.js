function userLogin(){
    let studName = document.getElementById("stuName").value;
    const studPass = document.getElementById("stuPass").value;

    const xmlhttp = new XMLHttpRequest();
    const method = 'GET';
    const url = 'http://127.0.0.1:5000/grades';

    xmlhttp.open(method, url, true);
    xmlhttp.send();
    xmlhttp.onload = function () {
        let loginDiv = document.getElementById("rcorners1");
        let loginBtn = document.getElementById("loginBtn");
        let signUpBtn = document.getElementById("signupBtn");
        
        for (let i = 0; i < classList.length; i++) {
            let person = classList[i].name;
            if(person == stuName){
                // let grade = classList[i].grade;
                if(stuPass = classList[i].password){
                    loginDiv.classList.add("hide");
                    loginDiv.classList.add("hide");
                    signUpBtn.classList.add("hide");
                }
                
            } 
        }
    };
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