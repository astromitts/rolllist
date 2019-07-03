function refresh(){
	window.location.reload();
}

function bind_delete_item(){
	// Handle opening the modal for the schedule view functions
	$('a.js-delete').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		$.ajax({
			type: 'GET',
			url: target_url,
			success: function(data){
				$('div#modalcontent').html(data);
				show_modal_and_overlay();
				bind_ajax_form_submit($('form.ajaxme'), target_url, refresh);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

function bind_edit_item(){
	$('a.js-edit').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		$.ajax({
			type: 'GET',
			url: target_url,
			success: function(data){
				$('div#modalcontent').html(data);
				var start_init = $('input#id_start_time_init').val();
				var end_init = $('input#id_end_time_init').val();

				$('select#id_end_time').val(end_init);
				$('select#id_start_time').val(start_init);

				show_modal_and_overlay();
				bind_ajax_form_submit($('form.ajaxme'), target_url, refresh);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

$(document).ready(function(){
	bind_delete_item();
	bind_edit_item();
});