

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
	});
}

function pad2(n) {
  z = '0';
  n = n + '';
  return n.length >= 2 ? n : new Array(2 - n.length + 1).join(z) + n;
}

/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
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