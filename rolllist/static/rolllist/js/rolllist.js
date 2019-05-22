function set_dropdown_times(){
	var start_val = window.location.href.split("/")[5];
	$('#id_start_time').val(start_val);
	$('#id_end_time').val(start_val);
}

$(document).ready(function(){
	var on_additem_page = window.location.href.indexOf("additem") > 0;

	if (on_additem_page) {
		set_dropdown_times();
	}

});