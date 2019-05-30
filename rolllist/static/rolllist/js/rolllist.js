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
function handle_todo_action(action_url){
	$.ajax({
		url: action_url,
		type: 'GET',
		success: function(data){
			get_todo_table();
		},
	});

}
function bind_todo_generic_handlers(){
	$('input.todo-generic').click(function(event){
		event.preventDefault();
		var action_url = $(this).attr('id');
		handle_todo_action(action_url);
	});
	$('a.todo-generic').click(function(event){
		event.preventDefault();
		var action_url = $(this).attr('href');
		handle_todo_action(action_url);
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

function get_tab_location(current_href){
	var current_location = current_href.split('#')[1];
	if (current_location == undefined) {
		current_location = 'schedulecontainer'
	}
	return current_location;
}

function update_href(current_href, new_location){
	if (current_href.indexOf('#') < 0){
		var new_href = current_href + '#' + new_location; 
	} else {
		var current_location = get_tab_location(current_href);
		var new_href = current_href.replace(current_location, new_location); 
	}
	return new_href;
}


function update_nav_with_tab_location(new_location){
	$('a.daytoggle').each(function(){
		var current_href = $(this).attr('href');
		var new_href = update_href(current_href, new_location);
		 $(this).attr('href', new_href);
	});
}

function update_window_with_tab_location(new_location){
	var current_href = this.window.location.href;
	var new_href = update_href(current_href, new_location);
	this.window.location.href = new_href;
}

function switch_target_container(target_id) {

	var this_button = $('button#toggle-' + target_id);
	var target_id = this_button.attr('id').replace('toggle-','');
	var target_div = $('#' + target_id);

	$('.toggle-target').hide();
	target_div.show();

	$('button.toggle-btn').addClass('btn-outline-primary');
	$('button.toggle-btn').removeClass('btn-primary');
	this_button.removeClass('btn-outline-primary');
	this_button.addClass('btn-primary');
	update_window_with_tab_location(target_id);
	update_nav_with_tab_location(target_id);
}

function bind_toggle_buttons(){
	var current_location = get_tab_location(window.location.href);
	switch_target_container(current_location);

	$('button.toggle-btn').click(function(){
		var target_id = $(this).attr('id').replace('toggle-','');
		switch_target_container(target_id);
	});
}

$(document).ready(function(){
	var on_additem_page = window.location.href.indexOf("additem") > 0;

	if (on_additem_page) {
		set_dropdown_times();
	}
	var datestr = $('div#datestr').text();
	get_schedule_table();
	get_todo_table();
	bind_toggle_buttons();
});