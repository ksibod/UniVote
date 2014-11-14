// Javascript for the register.html and registered.html files


// Function to cancel the popup for create account
function cancel()
{
    $("#modal").fadeOut("slow");
    $("#createUser").fadeOut("slow");

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
                 type: "success"},
                 function() {
                    $.ajax({
                        url: "",
                        context: document.body,
                        success: function(){

                        }
                    });
                 });
    }, 500);
}