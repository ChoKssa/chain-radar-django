const form = document.getElementById('login-form');

form.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Extract form data as key-value pairs
    const formData = new FormData(form);
    const values = Object.fromEntries(formData.entries());
    const { email, password } = values;

    // Retrieve users from local storage
    const users = JSON.parse(localStorage.getItem('users')) || [];

    // Check if user exists
    const user = users.find((user) => user.email === email);

    if (user) {
        // Check if password is correct
        if (user.password === password) {
            alert('Login successful');
        } else {
            alert('Invalid password');
        }
    } else {
        alert('User not found');
    }
});
