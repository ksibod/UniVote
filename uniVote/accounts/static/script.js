$(document).ready(function() {
	dothefunc();
});

function dothefunc()
{
	$("#uniLogo").fadeIn("3000");
	$("#login").slideToggle("slow");
	console.log("yolo dawg");
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
    return false;
}