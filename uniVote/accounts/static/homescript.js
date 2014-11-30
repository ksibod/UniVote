$(document).ready(function() {
	dothefunc();

	// when the user clicks on the register to vote button
    $("form.regToVoteForm").submit(function(request)
    {
        request.preventDefault();

        var election_id = $(this).find("input:hidden").val();
        console.log(election_id);
        var logForm = $(this);

        swal({
          title: "Are you sure?",
          text: "Click 'Register' below if you want to apply to register to vote in this election.",
          type: "warning",
          showCancelButton: true,
          confirmButtonColor: "#DD6B55",
          confirmButtonText: "Register",
          cancelButtonText: "Cancel",
          closeOnConfirm: false,
          closeOnCancel: false
        },
        function(isConfirm){
          if (isConfirm) {
                // ajax call here for the login
                $.ajax({
                    url: logForm.attr('action'),
                    type: logForm.attr('method'),
                    data: logForm.serialize(),
                    dataType: 'text',
                    success: function(response){
                        // code to update DOM here
                        console.log(response);
                        if (response === "registeredVoter") swal("Success!", "We will notify you when you have been approved to vote in this election.", "success");
                        else if (response === "loginFail") invalidCredentials();
                    },
                    error: function(response){
                        // log ajax errors?  something went wrong
                        console.log(response);
                        somethingWrong();
                    }
                });
          } else {
                swal("Cancelled", "You did not apply to vote in this election.", "error");
          }
        });

        return false;
    });

});

function dothefunc()
{
	$("#uniLogo").fadeIn("3000");
};



// Something went wrong server side in the AJAX call
function somethingWrong()
{
    swal({   title: "Oops...",
             text: "Something went wrong. Please try again!",
             type: "error"});
}