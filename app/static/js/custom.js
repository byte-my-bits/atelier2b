$(document).ready(function() {
    console.log("Ready!");


    // Manage edit-name-button text
    $('#edit-name').on('hide.bs.collapse', function() {
        $('a.edit-name-button').html("Edit");
    });
    $('#edit-name').on('show.bs.collapse', function() {
        $('a.edit-name-button').html("Close");
    });

     // Manage edit-dept-button text
     $('#edit-dept').on('hide.bs.collapse', function() {
        $('a.edit-dept-button').html("Edit");
    });
    $('#edit-dept').on('show.bs.collapse', function() {
        $('a.edit-dept-button').html("Close");
    });


    // Validate password
    $("#submit-button").click(function(event) {
        var pass = $("#pass").val();
        var confirmation = $("#confirmation").val();
        var regex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$/;
        if (!pass.match(regex)) {
            event.preventDefault();
            alert("Password must be 8-32 characters long and contain at least one number and one special character.");
        } else if (pass != confirmation) {
            event.preventDefault();
            alert("Password and confirmation do not match. Please re-enter them and try again.");
        }
    });


    // Resend validation email
    $("a.verify-button").click(function(event) {
        event.preventDefault();
        $(this).html("Sending email");
        $(this).css('pointer-events', 'none');
        $(this).addClass("text-muted");
        $.post("/verify", $("form.verify-form").serialize())
            .done(function(response) {
                console.log(response);
                $("a.verify-button").html("Email sent");
            })
            .fail(function(response) {
                console.log(response)
            });
    });

    
    // Add Role
    $("button.add-role-button").click(function() {
        $.post("/add_role", $("form.change-role-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });

    // Clear Roles
    $("button.clear-roles-button").click(function() {
        $.post("/clear_roles", $("form.change-role-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });



    // Change Name
    $("button.change-name-button").click(function() {
        $.post("/change_name", $("form.change-name-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });

    // Change Role
    $("button.change-role-button").click(function() {
        $.post("/change_role", $("form.change-role-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });

    // Add note
    $("button.add-note-button").click(function() {
        $.post("/add_note", $("form.add-note-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Delete note
    $("button.delete-note-button").click(function() {
        $.post("/delete_note", $("form.delete-note-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Send message
    $("button.send-message-button").click(function() {
        $.post("/send_message", $("form.send-message-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Delete message
    $("button.delete-message-button").click(function() {
        $.post("/delete_message", $("form.delete-message-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Hide sent message
    $("button.hide-sent-message-button").click(function() {
        $.post("/hide_sent_message", $("form.hide-sent-message-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


  

    // Create Household
    $("button.create-project-button").click(function() {
        $.post("/create_project", $("form.create-project-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });

    // Add Household member
    $("button.add-member-button").click(function() {
        $.post("/add_project_member", $("form.add-member-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });
 
    // Remove Household member
    $("button.remove-member-button").click(function() {
        $.post("/delete_project_member", $("form.remove-member-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });

    // Update project details
    $(document).ready(function() {
    $('select[name="project_id"]').change(function() {
        var selectedProjectId = $(this).val();
        $.ajax({
            url: '/get_project_details',  // replace with your Python script URL
            method: 'POST',
            data: $("form.change-project-form").serialize(),
            success: function(response) {
                var selectedProjectDetails = response;
                // Build a string that includes all the properties you want to display
                var detailsHtml = '<p>Project Name: ' + selectedProjectDetails.name + '</p>' +
                                  '<p>Project ID: ' + selectedProjectDetails.id + '</p>' +
                                  '<p>Project Type: ' + selectedProjectDetails.type + '</p>';
                // If members is an array of objects, you can loop through it to display each member
                if (Array.isArray(selectedProjectDetails.members)) {
                    detailsHtml += '<p>Members:</p><ul>';
                    selectedProjectDetails.members.forEach(function(member) {
                        detailsHtml += '<li>' + member.first_name + ' ' + member.last_name + '</li>';
                    });
                    detailsHtml += '</ul>';
                }
                // Set the HTML of the #project-details div to the detailsHtml string
                $('#project-details').html(detailsHtml);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
    

     // Change Dept
     $("button.change-dept-button").click(function() {
        $.post("/change_dept", $("form.change-dept-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });



    // Delete account
    $("button.second-delete").click(function(event) {
        if (confirm("Are you sure you want to delete your account?")) {
            console.log("Deleting account");
            $.post("/delete_account", $("form.delete-account-form").serialize())
                .done(function(response) {
                    console.log(response);
                    location.href = "/";
                })
                .fail(function(response) {
                    console.log(response)
                });
        } else {
            event.preventDefault();
            $("div.delete-account").collapse("hide");
        }
    });


    // Toggle delete button
    $("div.delete-account").on('hide.bs.collapse', function() {
        $("div.account-card").removeClass("border-danger");
        $("div.account-card").addClass("border-secondary");
        $("p.delete-warning").removeClass("text-danger");
        $("button.first-delete").html("Delete account");
    });
    $("div.delete-account").on('show.bs.collapse', function() {
        $("div.account-card").removeClass("border-secondary");
        $("div.account-card").addClass("border-danger");
        $("p.delete-warning").addClass("text-danger");
        $("button.first-delete").html("Hide the red button!");
    });

});

