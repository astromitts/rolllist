function bind_delete_workflow() {
	$('a.js-delete').click(function(event){
		event.preventDefault();
		confirmed = confirm("Deleting this recurring event will delete it from your schedule for today and all future dates. Confirm?");
		var target_url = $(this).attr('href');
		if(confirmed == true) {
			$.ajax({
				type: 'GET',
				url: target_url,
				success: function(data){
					window.location.reload();
				},
				error: function(data){
					alert("There was an error, could not delete recurring item.");
				}
			});
		}
	});
}

$(document).ready(function(){
	bind_delete_workflow();
});