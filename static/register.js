$("#registerForm").submit(function(event){
	event.preventDefault();
	$.ajax({
        url: "/api/p/register",
        type: "post",
        data: $(this).serialize(),
        statusCode: {
            200: function() { window.location.replace("/"); },
            406: function() { $('#title').html("Passwords does not match!"); $('#title').attr('style', "color: #C42069;"); },
            409: function() { $('#title').html("Nick taken."); $('#title').attr('style', "color: #C42069;"); },
            400: function() { $('#title').html("Could not create user."); $('#title').attr('style', "color: #C42069;"); }
        }
	});
});