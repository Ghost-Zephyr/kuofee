
if (mode === "ai") {
	$.ajax({
        url: "/game/WalterPenny",
        type: "get"
	}).done(function(resp) { $("#gameRow").html(resp); });
}
else if (mode === "pvp")
    $('#title').html("PvP quick play not implemented yet.");
else
    $('#title').html("Not accepted quick play mode!");

