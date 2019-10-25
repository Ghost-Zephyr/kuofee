$("#playerOpt").click(function() {
    $("#updatePlayerForm").attr("style", "");
});

$("#updatePlayerForm").submit(function(event) {
    event.preventDefault();
	$.ajax({
        url: "/api/p/update",
        type: "put",
        data: $(this).serialize(),
        statusCode: {
            200: function() { $('#tmp').html("HTTP 200!"); },
            401: function() { $('#tmp').html("Wrong password!"); $('#tmp').attr('style', "color: #C42069;"); },
            400: function() { $('#tmp').html("No such user."); $('#tmp').attr('style', "color: #C42069;"); }
        }
	}).done(function() { $(this).attr("style", "visibility: collapse"); });
});
// $("#updatePlayerForm").serialize()