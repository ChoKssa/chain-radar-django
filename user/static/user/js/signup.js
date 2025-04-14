/* ----------------------------
FORM VALIDATION FUNCTION
---------------------------- */
const form = document.getElementById('signup-form');

// Function to validate form inputs
const isValidForm = (values) => {
    // Regular expression for a valid email format
    const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    // Destructuring form values
    const { username, email, password1, password2, first_name, last_name, date_of_birth } = values;

    // Check if username is not empty
    if (username === '') {
        alert('Please enter a username');
        return false;
    }

    // Check if email format is valid
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return false;
    }

    // Check if password length is at least 6 characters
    if (password1.length < 6) {
        alert('Password must be at least 6 characters');
        return false;
    }

    // Check if password and confirm password match
    if (password1 !== password2) {
        alert('Passwords do not match');
        return false;
    }

    // Check if name has at least 3 characters
    if (first_name.length < 3) {
        alert('Name must be at least 3 characters');
        return false;
    }

    // Check if last name has at least 3 characters
    if (last_name.length < 3) {
        alert('Last name must be at least 3 characters');
        return false;
    }

    // Check if date of birth is not empty
    if (date_of_birth === '') {
        alert('Please enter your date of birth');
        return false;
    }

    // If all conditions pass, return true
    return true;
};

/* ----------------------------
    FORM SUBMISSION HANDLER
    ---------------------------- */
form.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Extract form data as key-value pairs
    const formData = new FormData(e.target);
    const values = {};

    // Convert FormData to a JavaScript object
    formData.forEach((value, key) => {
        values[key] = value;
    });

    // Validate the form data
    if (isValidForm(values)) {
        console.log('Form submitted successfully:', values);
        form.submit()
    }
});

/* ----------------------------
    PASSWORD VISIBILITY TOGGLE
    ---------------------------- */
const password = document.getElementById('password1');
const confirmPassword = document.getElementById('password2');
const showPassword = document.getElementById('show-password');
const hidePassword = document.getElementById('hide-password');
const showConfirmPassword = document.getElementById('show-confirm-password');
const hideConfirmPassword = document.getElementById('hide-confirm-password');

// Function to toggle password visibility
const togglePasswordVisibility = () => {
    if (showPassword.classList.contains("hidden")) {
        showPassword.classList.remove("hidden");
        hidePassword.classList.add("hidden");
        password.type = "text";
    } else {
        showPassword.classList.add("hidden");
        hidePassword.classList.remove("hidden");
        password.type = "password";
    }
};

// Function to toggle confirm password visibility
const toggleConfirmPasswordVisibility = () => {
    if (showConfirmPassword.classList.contains("hidden")) {
        showConfirmPassword.classList.remove("hidden");
        hideConfirmPassword.classList.add("hidden");
        confirmPassword.type = "text";
    } else {
        showConfirmPassword.classList.add("hidden");
        hideConfirmPassword.classList.remove("hidden");
        confirmPassword.type = "password";
    }
};

// Add event listeners for password toggle buttons
showPassword.addEventListener('click', togglePasswordVisibility);
hidePassword.addEventListener('click', togglePasswordVisibility);
showConfirmPassword.addEventListener('click', toggleConfirmPasswordVisibility);
hideConfirmPassword.addEventListener('click', toggleConfirmPasswordVisibility);
