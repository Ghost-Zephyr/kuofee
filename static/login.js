$("#loginForm").submit(function(event){
	event.preventDefault();
	$.ajax({
        url: "/api/p/login",
        type: "post",
        data: $(this).serialize(),
        statusCode: {
            200: function() { window.location.replace("/"); },
            401: function() { $('#title').html("Wrong password!"); $('#title').attr('style', "color: #C42069;"); },
            400: function() { $('#title').html("No such user."); $('#title').attr('style', "color: #C42069;"); }
        }
	});
});
