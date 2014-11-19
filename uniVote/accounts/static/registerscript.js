// Javascript for the register.html and registered.html files

$(document).ready(function() {

    // Intercept the submission of the register form
    $("#regForm").submit(function(request)
    {
        console.log("form stuff!");

        request.preventDefault();
        var regForm = $(this);

        // ajax call here for the login
        $.ajax({
            url: regForm.attr('action'),
            type: regForm.attr('method'),
            data: regForm.serialize(),
            dataType: 'text',
            success: function(response){
                // code to update DOM here
                console.log(response);
                if (response === "registerSuccess") {
                    $("#modal").hide();
                    $("#createUser").hide();

                    // reset the form to delete the fields
                    document.getElementById("regForm").reset();
                    showRegistered();
                }
                else if (response === "password_mismatch") {
                    $("#modal").hide();
                    $("#createUser").hide();
                    setTimeout(function() {
                        swal({   title: "Oops...",
                                 text: "There are blank fields or the passwords you entered did not match.",
                                 type: "error"},
                                 function(){
                                    $("#modal").show();
                                    $("#createUser").show();
                                 });
                    }, 500);
                }
            },
            error: function(response){
                // log ajax errors?  something went wrong
                console.log(response);
            }
        });

        console.log("done!");
    });

});



// Function to cancel the popup for create account
function cancel()
{

    $("#modal").fadeOut("fast");
    $("#createUser").fadeOut("fast");

    // reset the form to delete the fields
    document.getElementById("regForm").reset();
}

// Show that the user registered
function showRegistered()
{
    setTimeout(function() {
        swal({   title: "Awesome!",
                 text: "You have successfully created an account. Click below to login!",
                 confirmButtonColor: "#DD6B55",
                 confirmButtonText: "Login",
                 type: "success"
        });
    }, 500);
}



