$(document).ready(function() {
	dothefunc();

});

function dothefunc()
{
	$("#uniLogo").fadeIn("3000");
};

    // when the user clicks on the register to vote button
function registerToVote(election_id)
{
    console.log(election_id);

    swal({
      title: "Are you sure?",
      text: "You will not be able to recover this imaginary file!",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: "#DD6B55",
      confirmButtonText: "Yes, delete it!",
      cancelButtonText: "No, cancel plx!",
      closeOnConfirm: false,
      closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm) {
        swal("Deleted!", "Your imaginary file has been deleted.", "success");
      } else {
            swal("Cancelled", "Your imaginary file is safe :)", "error");
      }
    });

    return false;
};