const signUpPageLink = document.querySelector('#signup-page-link');
const loginPageLink = document.querySelector('#login-page-link');
const wrapper = document.querySelector('.wrapper');

const signUpButton = document.querySelector('#signup-button');
const signUpEmail = document.querySelector('#signup-email');
const signUpPassword = document.querySelector('#signup-password');
const signUpName = document.querySelector('#signup-name');

const loginButton = document.querySelector('#login-button');
const loginEmail = document.querySelector('#login-email');
const loginPassword = document.querySelector('#login-password');

const signoutButton = document.querySelector('#signout-button');

const signupWarning = document.querySelector('#signup-warning');
const loginWarning = document.querySelector('#login-warning');

loginPassword.addEventListener('input', checkLoginButton);
signUpPassword.addEventListener('input', checkSignUpButton);
loginEmail.addEventListener('input', checkLoginButton);
signUpEmail.addEventListener('input', checkSignUpButton);
signUpName.addEventListener('input', checkSignUpButton);

function checkLoginButton() {
    if (loginPassword.value.length >= 6 && loginEmail.value !== "") {
        loginButton.style.backgroundColor = "#0095f6";
    } else {
        loginButton.style.backgroundColor = "#bcdffc";
    }
}

function checkSignUpButton() {
    if (signUpPassword.value.length >= 6 && signUpEmail.value !== "" && signUpName.value !== "") {
        signUpButton.style.backgroundColor = "#0095f6";
    } else {
        signUpButton.style.backgroundColor = "#bcdffc";
    }
}

signUpPageLink.addEventListener('click', function () {
    wrapper.style.top = '-100%';
});

loginPageLink.addEventListener('click', function () {
    wrapper.style.top = '0%';
});


const firebaseConfig = {
    apiKey: "AIzaSyCnWbrjWukZRLmPF6uWqR4Wo_3m-rtz2hI",
    authDomain: "web-tai-6ebaa.firebaseapp.com",
    databaseURL: "https://web-tai-6ebaa-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "web-tai-6ebaa",
    storageBucket: "web-tai-6ebaa.appspot.com",
    messagingSenderId: "149766567228",
    appId: "1:149766567228:web:202ecd644d35a3c251da39"
  };

firebase.initializeApp(firebaseConfig);
const database = firebase.database();
const auth = firebase.auth()


signUpButton.addEventListener('click', function () {
    signUpButton.innerText = 'Loading...';

    // Clear any previous warning messages
    signupWarning.innerText = '';

    auth.createUserWithEmailAndPassword(signUpEmail.value, signUpPassword.value)
        .then((userCredential) => {
            signUpButton.innerText = 'Sign Up';
            var currentUser = auth.currentUser;
            currentUser.updateProfile({
                displayName: signUpName.value,
            });
        })
        .catch((error) => {
            signUpButton.innerText = 'Sign Up';
            if (error.code === 'auth/invalid-email') {
                signupWarning.innerText = 'The email address is badly formatted.';
            } else {
                // Handle other errors here if needed
                signupWarning.innerText = error.message;
            }
        });
});


loginButton.addEventListener('click', function () {
    loginButton.innerText = 'Loading...';

    // Clear any previous warning messages
    loginWarning.innerText = '';

    auth.signInWithEmailAndPassword(loginEmail.value, loginPassword.value)
        .then(() => {
            loginButton.innerText = 'Log In';
        })
        .catch((error) => {
            loginButton.innerText = 'Log In';
            if (error.code === 'auth/invalid-email') {
                loginWarning.innerText = 'The email address is badly formatted.';
            } else {
                // Handle other errors here if needed
                loginWarning.innerText = error.message;
            }
        });
});


signoutButton.addEventListener('click', function () {
    auth.signOut()
        .then(() => {
            // Sign-out successful.
        })
        .catch((error) => {
            // An error happened.
        });
});

auth.onAuthStateChanged((user) => {
    wrapper.style.top = '0';
    loginPassword.value = '';
    loginEmail.value = '';
    signUpPassword.value = '';
    signUpEmail.value = '';

    if (user) {
        wrapper.style.display = 'none';
    } else {
        wrapper.style.display = 'block';
    }
});
