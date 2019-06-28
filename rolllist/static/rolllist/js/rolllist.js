/* OVERLAY & MODAL HANDLERS */

function show_modal_and_overlay(){
	// Display the gray overlay and the modal container
	$('div#modal').css('display', 'inline-block');
	$('div#backgroundcover').show();
}

function hide_modal_and_overlay(){
	// Hide all overlay and modal components and blank out the modal contents
	$('div#modal').hide();
	$('div#modalcontent').html();
	$('div#backgroundcover').hide();
	window.scrollTo(0, 0);
}

function bind_modal_close(){
	// bind the hide functions to the close element of the modal
	$('a.closemodal').click(function(event){
		event.preventDefault();
		hide_modal_and_overlay();
	});
}

function bind_ajax_form_submit(form, action, reload_function){
	// bind a form submit to the ajax submit and refresh function
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



/* NAVIGATION HANDLERS */
function get_tab_location(current_href){
	// figure out the current tab by the URL anchor
	var current_location = current_href.split('#')[1];
	if (current_location == undefined) {
		current_location = 'schedule-collapse'
	}
	return current_location;
}

function update_href(current_href, new_location){
	// Figure out what the window URL should be with a new tab's anchor
	if (current_href.indexOf('#') < 0){
		var new_href = current_href + '#' + new_location; 
	} else {
		var current_location = get_tab_location(current_href);
		var new_href = current_href.replace(current_location, new_location); 
	}
	return new_href;
}

function update_nav_with_tab_location(new_location){
	// Update the HREF of nav links with anchor for new location
	$('a.daytoggle').each(function(){
		var current_href = $(this).attr('href');
		var new_href = update_href(current_href, new_location);
		$(this).attr('href', new_href);
	});
}

function update_window_with_tab_location(new_location){
	// Update the URL of the window with anchor for new location
	var current_href = this.window.location.href;
	var new_href = update_href(current_href, new_location);
	this.window.location.href = new_href;
}

// ##############  START display style of the schedule table ##########	
function fully_collapse_schedule_table(){
	// fully hide the schedule table
	$('div#schedule').hide();
	$('a#schedule-hide').hide();
	$('a#schedule-show').show();
}

function hide_schedule_table(){
	// don't show the schedule table at all
	$('div#schedule').hide();
}

function expand_schedule_table(){
	// show the full schedule table
	$('div#schedule').show();
	$('table.schedule-open').show();
}

function collapse_schedule_table(){
	// show only scheduled items of the schedule table
	$('div#schedule').show();
	$('table.schedule-open').hide();
}

function toggle_schedule_display(selected){
	var action = selected.attr('id');
	$('button.schedule-control').each(function(){
		$(this).removeClass('schedule-control-selected');
		$(this).removeClass('btn-info');
		$(this).addClass('btn-outline-info');
	});
	selected.addClass('schedule-control-selected');
	selected.removeClass('btn-outline-info');
	selected.addClass('btn-info')

	if (action == 'schedule-hide') {
		hide_schedule_table();
	} else if (action == 'schedule-expand') {
		expand_schedule_table();
	} else if (action == 'schedule-collapse') { 
		collapse_schedule_table();
	}
	update_window_with_tab_location(action);
	update_nav_with_tab_location(action);
}

function bind_schedule_controls(){
	$('button.schedule-control').click(function(event){
		event.preventDefault();
		var selected = $(this);
		toggle_schedule_display(selected);
	});
}

function init_schedule_display(){
	// on schedule table load set schedule display to default or pre-selected val
	anchored_location = get_tab_location(this.window.location.href);
	selected = $('button#' + anchored_location);
	toggle_schedule_display(selected);
	update_window_with_tab_location(selected.attr('id'));
	update_nav_with_tab_location(selected.attr('id'));
}


// ##############  END display style of the schedule table ##########

/* SCHEDULE VIEW HANDLERS */
function bind_modal_open_schedule(datestr){
	// Handle opening the modal for the schedule view functions
	$('a.openmodalschedule').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		var start_val = $(this).attr('id');
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
				bind_ajax_form_submit($('form.ajaxme'), target_url, get_schedule_table, datestr);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}


function bind_schedule_generic_handlers(){
	// Bind ajax workflow to schedule actions
	$('a.schedulegeneric').click(function(event){
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
	// Load or refresh the schedule table div contents from ajax call
	$.ajax({
		url: $('div#get_schedule').text(),
		type: 'GET',
		success: function(data){
			$('div#schedulecontainer').html(data);
			bind_modal_open_schedule();
			bind_schedule_generic_handlers();
			bind_modal_close();
			bind_schedule_controls();
			init_schedule_display();
		},
	})
}

/* TO DO VIEW HANDLERS */

function bind_modal_open_todo(datestr){
	// Handle the modal opening function for the to-do view
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

function handle_todo_action(action_url){
	// Handle refreshing the to-do container
	$.ajax({
		url: action_url,
		type: 'GET',
		success: function(data){
			get_todo_table();
		},
	});

}
function bind_todo_generic_handlers(){
	// Bind generic todo handler to action links for 
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
	// load & refresh the to-do list view
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


/* NOTES VIEW HANDLERS */

function bind_notes_form_handlers(){
	// handle ajax form show & submit for notes form
	$('a.notes-generic').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		$.ajax({
			type: 'GET',
			url: target_url,
			success: function(data){
				$('div#modalcontent').html(data);
				show_modal_and_overlay();
				bind_ajax_form_submit($('form.ajaxme'), target_url, get_notes_table, datestr);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

function get_notes_table(){
	// load & refresh the notes view
	$.ajax({
		url: $('div#get_notes').text(),
		type: 'GET',
		success: function(data){
			$('span#notescontainer').html(data);
			bind_notes_form_handlers();
			bind_modal_close();
		},
	})
}

/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
	get_schedule_table();
	get_todo_table();
	get_notes_table();
});