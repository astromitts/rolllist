function show_modal_and_overlay(){
	$('div#modal').css('display', 'inline-block');
	$('div#backgroundcover').show();
}

function hide_modal_and_overlay(){
	$('div#modal').hide();
	$('div#backgroundcover').hide();
}

function bind_ajax_form_submit(form, action, reload_function){
	form.submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: action,
			data: $(this).serialize(),
			success: function(data){
				reload_function(datestr);
				hide_modal_and_overlay();
			},
			error: function(data){
				hide_modal_and_overlay();
				alert("there was an error");
			}
		});
	});
}

function bind_modal_open_schedule(datestr){
	$('a.openmodalschedule').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		var start_val = $(this).attr('id');
		$.ajax({
			type: 'GET',
			url: target_url,
			success: function(data){
				$('div#modalcontent').html(data);

				$('#id_start_time').val(start_val);
				$('#id_end_time').val(parseInt(start_val) + 1);
				
				show_modal_and_overlay();
				bind_ajax_form_submit($('form.ajaxme'), target_url, get_schedule_table, datestr);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}



function bind_modal_open_todo(datestr){
	$('a.openmodaltodo').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		$.ajax({
			type: 'GET',
			url: target_url,
			success: function(data){
				$('div#modalcontent').html(data);
				show_modal_and_overlay();
				bind_ajax_form_submit($('form.ajaxme'), target_url, get_todo_table, datestr);
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
		hide_modal_and_overlay();
	});
}

function bind_schedule_generic_handlers(){
	$('a.schedule-generic').click(function(event){
		event.preventDefault();
		var action = $(this).attr('href');
		$.ajax({
			url: action,
			type: 'GET',
			success: function(data){
				get_schedule_table();
			},
		})
	});
}

function get_schedule_table(){
	$.ajax({
		url: $('div#get_schedule').text(),
		type: 'GET',
		success: function(data){
			$('div#schedulecontainer').html(data);
			bind_modal_open_schedule();
			bind_schedule_generic_handlers();
			bind_modal_close();
		},
	})
}

function bind_todo_generic_handlers(){
	$('a.todo-generic').click(function(event){
		event.preventDefault();
		var action = $(this).attr('href');
		$.ajax({
			url: action,
			type: 'GET',
			success: function(data){
				get_todo_table();
			},
		})
	});
}

function get_todo_table(){
	$.ajax({
		url: $('div#get_todo').text(),
		type: 'GET',
		success: function(data){
			$('span#todocontainter').html(data);
			bind_modal_open_todo();
			bind_todo_generic_handlers()
			bind_modal_close();
		},
	})
}

$(document).ready(function(){
	var on_additem_page = window.location.href.indexOf("additem") > 0;

	if (on_additem_page) {
		set_dropdown_times();
	}
	var datestr = $('div#datestr').text();
	get_schedule_table();
	get_todo_table();

});