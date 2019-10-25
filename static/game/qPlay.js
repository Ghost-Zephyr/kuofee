
if (mode === "ai") {
    // TODO: add dice game alternative to Penny's game
	$.ajax({
        url: "/game/WalterPenny",
        type: "get"
	}).done(function(resp) { $("#gameRow").html(resp); });
}
else if (mode === "pvp")
    $('#title').html("PvP quick play not implemented yet.");
else
    window.location.replace("/");

