
var login_btn = document.getElementById("login_btn");
var forgotPW_lnk = document.getElementById("forgotPW_lnk");
var newAcct_lnk = document.getElementById("newAcct_lnk");

$(document).on("click", "forgotPW_lnk", function(){
	//redirect to the correct page (needs developed)
});

document.getElementById("login_btn").disabled = true;


//document.getElementById("create_account_btn").addEventListener("click", function(event) {
document.getElementById("create_account_btn").addEventListener("click", function(event) {    
    var email = document.getElementById("email").value;
    var confirmEmail = document.getElementById("confirm_email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;

    if (email !== confirmEmail) {
        alert("⚠️ Emails do not match!");
        event.preventDefault();  // Stop form submission
        return;
    }

    if (password !== confirmPassword) {
        alert("⚠️ Passwords do not match!");
        event.preventDefault();  // Stop form submission
        return;
    }

    // Allow form submission if everything is valid
});

document.addEventListener("DOMContentLoaded", function () {
    // Get the 'Create New Account' link and add an event listener
    var newAcctLnk = document.getElementById("newAcct_lnk");

    if (newAcctLnk) {
        newAcctLnk.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior
            var createUserModal = new bootstrap.Modal(document.getElementById("createUserModal"));
            createUserModal.show(); // Show the modal
        });
    }

    // Enable form inputs when modal is shown
    document.getElementById("createUserModal").addEventListener("shown.bs.modal", function () {
        document.getElementById("registerForm").querySelectorAll("input").forEach(function (input) {
            input.removeAttribute("disabled"); // Ensure form fields are enabled
        });
    });
});








