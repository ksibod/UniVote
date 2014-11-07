$(document).ready(function() {
	dothefunc();
});

function dothefunc()
{
	$("#uniLogo").fadeIn("3000");
	$("#login").fadeIn("3000");
}


// Function to show incorrect credentials popup on login page
function invalidCredentials()
{
    console.log("INVALID!");
    setTimeout(function() {
        swal({   title: "Oops...",
                 text: "Your username or password is invalid. Please try again.",
                 type: "error"});
    }, 500);
    console.log("showing the popup");
}


// Function to show the popup when the create account button is pressed on the login page
function createAccount()
{
    $("#createUser").fadeIn("slow");
}