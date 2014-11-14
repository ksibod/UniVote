$(document).ready(function() {
	dothefunc();


	// Intercept the submission of the login form
    $("form #loginForm").submit(function(request)
    {
        console.log("form stuff!");

        request.preventDefault();
        var logForm = $(request.target);
        $.ajax({
            url: user_login.attr('action'),
            type: user_login.attr('method'),
            data: user_login.serialize(),
            dataType: 'json',
            success: function(json){
                // code to update DOM here

            },
            error: function(xhr, ajaxOptions, thrownError){
                // log ajax errors?
                invalidCredentials();
            }
        });

        console.log("done!");
    });


});

function dothefunc()
{
	$("#uniLogo").fadeIn("3000");
	$("#login").fadeIn("3000");
	$("#createUser").load("accounts/register");
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
    $("#modal").fadeIn("slow");
    $("#createUser").fadeIn("slow");
}







// tooltip for forgot password (shows when the user is typing in the password or clicks on the password box)
$("#passwordLogin").tooltip({
    position: { my: "right center", at: "left-10 center" },
    show: {
        delay: 250
    },
    content: "<a id='forgotPassword' href='#' onclick='forgotPassword();'>Forgot Password?</a>",
    close: function(event, ui){
        ui.tooltip.hover(
            function () {
                $(this).stop(true).fadeTo(400, 1);
            },
            function () {
                $(this).fadeOut("400", function(){
                    $(this).remove();
                })
            }
        );
    }
 });



