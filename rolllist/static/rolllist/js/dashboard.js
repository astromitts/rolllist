/* DISPLAY HANDLERS */
function get_anchor(){
	// function to get the persisted display setting, otherwise default to collapsed
	var anchor = Cookies.get('_rollist-anchor');
	if (anchor == 'undefined' || anchor == undefined) {
		anchor = 'js-schedule-collapse';
	}
	return anchor;
}

function expand_schedule_table(){
	// show the full schedule table
	$('div.toggle-open').show();
	// $('button#js-schedule-hide').show();
	$('button#js-schedule-expand').hide();
	$('button#js-schedule-collapse').show();
}

function collapse_schedule_table(){
	// show only scheduled items of the schedule table
	$('div.toggle-open').hide();
	// $('button#js-schedule-hide').hide();
	$('button#js-schedule-expand').show();
	$('button#js-schedule-collapse').hide();
}

function toggle_schedule_display(selected){
	var action = selected.attr('id');
	$('button.js-schedule-control').each(function(){
		$(this).removeClass('js-schedule-control-selected');
	});
	selected.addClass('js-schedule-control-selected');

	if (action == 'js-schedule-expand') {
		expand_schedule_table();
	} else if (action == 'js-schedule-collapse') { 
		collapse_schedule_table();
	}
	Cookies.set('_rollist-anchor', action);
}

function bind_schedule_controls(){
	$('button.js-schedule-control').click(function(event){
		event.preventDefault();
		var selected = $(this);
		toggle_schedule_display(selected);
	});
	$('button.aslink').click(function(event){
		action = $(this).attr('action');
		location.href = action;
	});
}

function init_schedule_display(){
	// on schedule table load set schedule display to default or pre-selected val
	init_location = get_anchor();
	Cookies.set('_rollist-anchor', init_location);
	selected = $('button#' + init_location);
	toggle_schedule_display(selected);
}


// ##############  END display style of the schedule table ##########

/* SCHEDULE VIEW HANDLERS */
function bind_modal_open_schedule(datestr){
	// Handle opening the modal for the schedule view functions
	$('button.openmodalschedule').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('action');
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
				bind_all_day_toggle();
				bind_ajax_form_submit($('form.ajaxme'), target_url, get_schedule_table);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

function bind_all_day_toggle(){
	var init_checked = $('input#id_all_day').attr('checked') == "checked";

	if (init_checked) {
    	$('select#id_start_time').prop("disabled", true);
    	$('select#id_end_time').prop("disabled", true);
	}

	$('input#id_all_day').change(function() {
	    if(this.checked) {
	    	$('select#id_start_time').prop("disabled", true);
	    	$('select#id_end_time').prop("disabled", true);
	    } else {
	    	$('select#id_start_time').prop("disabled", false);
	    	$('select#id_end_time').prop("disabled", false);
	    }
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

function bind_show_hide_edit_links(){
	$('a.js-schedule-links-toggle').click(function(event){
		event.preventDefault();
		var links_div = $('div#js-schedule-links-toggle-' + $(this).attr('id'));
		if (links_div.is(":visible")) {
			links_div.hide();
		} else {
			links_div.show();
		}

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
			bind_show_hide_edit_links();
			init_schedule_display();
		},
	})
}

/* TO DO VIEW HANDLERS */

function bind_toggle_kanban_links(){
	$('a.js-open-kanban-links').click(function(event){
		event.preventDefault();
		var target_div = $('div#' + $(this).attr('id'));
		if (target_div.is(":visible")){
			target_div.hide();
		} else {
			target_div.show();
		}
		
	});
}

function bind_modal_open_todo(datestr){
	// Handle the modal opening function for the to-do view
	$('a.js-openmodal-todo').click(function(event){
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
	$('input.js-todo-generic').click(function(event){
		event.preventDefault();
		var action_url = $(this).attr('id');
		handle_todo_action(action_url);
	});
	$('a.js-todo-generic').click(function(event){
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
			$('div#todocontainter').html(data);
			bind_modal_open_todo();
			bind_todo_generic_handlers();
			bind_modal_close();
			bind_toggle_kanban_links();
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
			$('div#notescontainer').html(data);
			bind_notes_form_handlers();
			bind_modal_close();
		},
	})
}

function pad2(n) {
  z = '0';
  n = n + '';
  return n.length >= 2 ? n : new Array(2 - n.length + 1).join(z) + n;
}

/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
	get_schedule_table();
	get_todo_table();
	//get_notes_table();
	$(function () {
		$( "#datepicker" ).datepicker({
			format: "YYYYMMDD",
			showOn: "button",
			buttonImage: "{% static 'images/iconic/png/calendar-3x-orange.png' %}",
			buttonImageOnly: true
		}).on('changeDate', function(ev) {
        	var selected = $( "#datepicker" ).datepicker('getDate');
        	var day = pad2(selected.getDate());
        	var month = pad2(selected.getMonth() + 1);
        	var year = selected.getFullYear();
        	var current_date = $('div#datestr').text();
        	var new_date = year.toString() + month.toString() + day.toString();
        	var full_current_location = location.href;
        	if (full_current_location.indexOf(current_date) > 1) {
        		var full_target_location = full_current_location.replace(current_date, new_date);
        	} else {
        		var origin = window.location.origin;
        		var full_target_location = origin + '/' + new_date;
        	}
        	location.href = full_target_location;
    	});
	});
});