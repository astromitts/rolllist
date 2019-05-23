function set_dropdown_times(){
	var start_val = window.location.href.split("/")[5];
	$('#id_start_time').val(start_val);
	$('#id_end_time').val(start_val);
}

function bind_ajax_form_submit(action){
	$('form.ajaxme').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: action,
			data: $(this).serialize(),
			success: function(data){
				location.reload();
			},
			error: function(data){
				$('div#modal').hide();
				alert("there was an error");
			}
		});
	});
}

function bind_modal_open(){
	$('a.openmodal').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href')
		$.ajax({
			type: 'GET',
			url: target_url,
			success: function(data){
				$('div#modalcontent').html(data);
				$('div#modal').show();
				bind_ajax_form_submit(target_url);
			},
			error: function(data){
				alert("there was an error");
			}
		});
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
	}

	bind_modal_open();
	bind_modal_close();

});