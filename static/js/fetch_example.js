// const curr_main = document.querySelector('main');
// console.log(curr_main);
let str1 = 'Hello World!!!:)';

console.log(str1);

function myFunction() {
    fetch('https://reqres.in/api/users?page=2').then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}


function createUsersList(users){
    console.log(users);
    const user = users[0];
    console.log(user);
    const curr_main = document.querySelector("main");
    for(let user of users){
        const section = document.createElement('section');
        section.innerHTML = `
        <img src="${user.avatar}" alt="Profile Picture"/>
        <div>
            <span>${user.first_name} ${user.last_name}</span>
            <br>
            <a href="mailto:${user.email}">Send Email</a>
        </div>
        `;
        curr_main.appendChild(section);
    }
}

// function createUsersList(users){
//     const user = users[0];
//     console.log(user);
// }