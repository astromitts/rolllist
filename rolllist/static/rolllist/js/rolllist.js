function set_dropdown_times(){
	var start_val = window.location.href.split("/")[5];
	$('#id_start_time').val(start_val);
	$('#id_end_time').val(start_val);
}

function bind_modal_open(){
	$('a.openmodal').click(function(event){
		event.preventDefault();
		$('div#modal').show();
	});
}


function bind_modal_close(){
	$('a.closemodal').click(function(event){
		event.preventDefault();
		$('div#modal').hide();
	});
}

$(document).ready(function(){
	var on_additem_page = window.location.href.indexOf("additem") > 0;

	if (on_additem_page) {
		set_dropdown_times();
		$.ajax(

		)
	}

	bind_modal_open();
	bind_modal_close();

});