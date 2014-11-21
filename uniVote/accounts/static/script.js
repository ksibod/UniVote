$(document).ready(function() {


	dothefunc();


	// tooltip for forgot password (shows when the user is typing in the password or clicks on the password box)
    $("#passwordInput").tooltip({
        position: { my: "right center", at: "left-10 center" },
        show: {
            delay: 250
        },
        content: "<a id='forgotPassword' href='javascript:forgotPassword();'>Forgot Password?</a>",
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


// This function just fades in the image and login div and loads the register html file into its div
function dothefunc()
{
	$("#uniLogo").fadeIn("3000");
	$("#login").fadeIn("3000");
	$("#createUser").load("accounts/register");
}



// Function to show incorrect credentials popup on login page
function invalidCredentials()
{
    swal({   title: "Oops...",
             text: "Your username or password is invalid. Please try again.",
             type: "error"});
    console.log("showing the popup");
}



// Something went wrong server side in the AJAX call
function somethingWrong()
{
    swal({   title: "Oops...",
             text: "Something went wrong. Please try again!",
             type: "error"});
}



// Function to show the popup when the create account button is pressed on the login page
function createAccount()
{
    $("#modal").fadeIn("fast");
    $("#createUser").fadeIn("fast");
}




// Function to handle when the user clicks the "Forgot password" bubble tip
function forgotPassword()
{
    // Define the Dialog and its properties
    $("div#userEmail").dialog({
        resizable: false,
        draggable: false,
        dialogClass: "forgot",
        modal: false,
        width: 500,
        open: function () {;
        },
        buttons: {
            "Send": function () {

                $(this).dialog("close");
                startLoading();
                var form = $("#forgotEmailForm");

                // ajax call here for sending email notification
                $.ajax({
                    url: "accounts/password/reset/",
                    type: form.attr('method'),
                    data: form.serialize(),
                    dataType: 'text',
                    success: function(response){
                        // code to update DOM here
                        console.log(response);
                        stopLoading();
                        if (response === "resetFormSuccess") {
                            swal({   title: "Sent!",
                                text: "We've e-mailed you instructions for setting your password to the e-mail address you submitted. You should be receiving it shortly.",
                                type: "success"});
                        }
                    },
                    error: function(response){
                        // log ajax errors?  something went wrong
                        console.log(response);
                        somethingWrong();
                    }
                });


            },
            "Cancel": function () {
                $(this).dialog("close");
            }
        }
    });
}



// Function to show the loading gif
function startLoading () {
	$("#modal").fadeIn("fast");
	$("#loadingImg").fadeIn("fast");
};

function stopLoading () {
	$("#modal").fadeOut("fast");
	$("#loadingImg").fadeOut("fast");
};
