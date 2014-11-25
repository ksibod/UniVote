$(document).ready(function() {


	// Intercept the submission of the voting form
    $("#voteForm").submit(function(request)
    {
        console.log("form stuff!");

        request.preventDefault();
        var voteForm = $(this);

        // ajax call here for the login
        $.ajax({
            url: voteForm.attr('action'),
            type: voteForm.attr('method'),
            data: voteForm.serialize(),
            dataType: 'text',
            success: function(response){
                // code to update DOM here
                console.log(response);
                if (response === "anonymous") anonymousUser();
                else if (response === "noSelection") noCandidateSelected();
                else if (response === "alreadyVoted") alreadyVoted();
                else if (response === "userNotApproved") notApproved();
                else if (response === "done") voteSuccess();
            },
            error: function(response){
                // log ajax errors?  something went wrong
                console.log(response);
                somethingWrong();
            }
        });
    });

});


// function to tell the user to login
function anonymousUser()
{
    swal({   title: "Login!",
             text: "You must be logged in and registered to vote.",
             type: "error"
    });
};

// function to tell the user they didn't select a candidate
function noCandidateSelected()
{
    swal({   title: "Oops...",
             text: "You didn't select a candidate.",
             type: "error"
    });
};

// function to tell the user they already voted in this election
function alreadyVoted()
{
    swal({   title: "One time only!",
             text: "You are only allowed to vote once. You have already voted in this election.",
             type: "error"
    });
};



// Something went wrong server side in the AJAX call
function somethingWrong()
{
    swal({   title: "Oops...",
             text: "Something went wrong. Please try again!",
             type: "error"
    });
}


// user is not approved for this election
function notApproved()
{
    swal({   title: "Oops...",
             text: "You are not approved for this election.",
             type: "error"
    });
}


// Function to show the user they successfully voted and redirect to the elections page
function voteSuccess()
{
    swal({   title: "Voted!",
             text: "You have successfully entered your vote(s) in this election. Thank you! We have also sent you an email with a confirmation receipt of your vote.",
             type: "success"
    });

    window.location.href = "/elections";
}