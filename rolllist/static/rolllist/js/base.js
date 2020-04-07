function bind_close_message() {
	$('button.close-message').click(function(){
		$(this).parent('div.alert').hide();
	});
}

$(document).ready(function() {
	bind_close_message();
});