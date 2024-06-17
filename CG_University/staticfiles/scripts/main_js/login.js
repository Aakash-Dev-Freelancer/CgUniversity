document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("#admin-login form");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve the email and password entered by the user
    const email = document.querySelector("#admin-email").value;
    const password = document.querySelector("#admin-password").value;

    // Here, you can perform validation checks on the email and password if needed

    // Send the login credentials to the server for authentication
    loginUser(email, password);
  });

  function loginUser(email, password) {
    // Here you would typically make an AJAX request to your server
    // to send the login credentials and handle the authentication process
    // For demonstration purposes, I'll just log the credentials to the console
    console.log("Email: " + email);
    console.log("Password: " + password);

    // You can replace the console.log statements with your actual AJAX request
    // Example AJAX request:
    /*
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email, password: password }),
        })
        .then(response => {
            // Handle the response from the server
        })
        .catch(error => {
            console.error('Error:', error);
        });
        */
  }
});
