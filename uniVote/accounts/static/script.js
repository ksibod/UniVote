$(document).ready(function() {
	dothefunc();


	// tooltip for forgot password (shows when the user is typing in the password or clicks on the password box)
    $("#passwordInput").tooltip({
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


	// Intercept the submission of the login form
    $("#loginForm").submit(function(request)
    {
        console.log("form stuff!");

        request.preventDefault();
        var logForm = $(this);

        // ajax call here for the login
        $.ajax({
            url: logForm.attr('action'),
            type: logForm.attr('method'),
            data: logForm.serialize(),
            dataType: 'text',
            success: function(response){
                // code to update DOM here
                console.log(response);
                if (response === "loginSuccess") window.location.href = "/elections";
                else if (response === "loginFail") invalidCredentials();
            },
            error: function(response){
                // log ajax errors?  something went wrong
                console.log(response);
                somethingWrong();
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


// something went wrong server side
function somethingWrong()
{
    setTimeout(function() {
        swal({   title: "Oops...",
                 text: "Something went wrong. Please try again!",
                 type: "error"});
    }, 500);
}


// Function to show the popup when the create account button is pressed on the login page
function createAccount()
{
    $("#modal").fadeIn("fast");
    $("#createUser").fadeIn("fast");
}