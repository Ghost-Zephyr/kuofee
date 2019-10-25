$("#registerForm").submit(function(event){
    event.preventDefault();
    if ($("#pwd").serialize().slice(4) != $("#pwd1").serialize().slice(5)) {
        $('#title').html("Passwords does not match!");
        $('#title').attr('style', "color: #C42069;");
    }
    else {
        $.ajax({
            url: "/api/p/register",
            type: "post",
            data: $(this).serialize(),
            statusCode: {
                200: function() { window.location.replace("/"); },
                409: function() { $('#title').html("Nick taken."); $('#title').attr('style', "color: #C42069;"); },
                400: function() { $('#title').html("Could not create user."); $('#title').attr('style', "color: #C42069;"); }
            }
        });
    }
});