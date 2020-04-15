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

function schedule_toggled_view(show_button){

	var showdiv = $('div.' + show_button.attr('id'));
	var hidediv = $('div.' + show_button.attr('data-hide-div'));
	var new_show_button_id = show_button.attr('data-hide-div');
	var new_show_button = $('button#' + new_show_button_id);
	
	showdiv.show();
	hidediv.hide();
	show_button.hide();
	new_show_button.show();
	Cookies.set('_rollist-schedule-view', showdiv);
}

function init_schedule_toggled_view() {
	valid_toggle_options = ['table-toggled-view_full', 'table-toggled-view_collapsed'];
	var show_button_id = Cookies.get('_rollist-schedule-view');
	if ($.inArray(show_button_id, valid_toggle_options) < 0) {
		show_button_id = valid_toggle_options[0];
	}
	var show_button = $('button#' + show_button_id);
	schedule_toggled_view(show_button);
	$('button.js-schedule-toggle').click(function(){
		schedule_toggled_view($(this));
	});
}


// ##############  END display style of the schedule table ##########


/* SCHEDULE VIEW HANDLERS */
function bind_delete_from_modal(delete_url){
	$('form#schedule_delete').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: delete_url,
			data: $(this).serialize(),
			success: function(data){
				get_schedule_table();
				hide_modal_and_overlay();
			},
			error: function(data){
				alert("there was an error");
				hide_modal_and_overlay();
			}
		});
	});
}

function bind_edit_from_modal(edit_url){
	$('form#schedule_edit').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: edit_url,
			data: $(this).serialize(),
			success: function(data){
				get_schedule_table();
				hide_modal_and_overlay();
			},
			error: function(data){
				alert("there was an error");
				hide_modal_and_overlay();
			}
		});
	});
}

function bind_modal_open_schedule_options(datestr){
	// Handle opening the modal for the schedule view functions
	$('div.js-edit-item').click(function(){
		var edit_url = $(this).attr('data-edit-url');
		var delete_url = $(this).attr('data-delete-url');
		var is_recurring = $(this).attr('data-recurring-item');
		var start_val = $(this).attr('id');
		$.ajax({
			type: 'GET',
			url: edit_url,
			data: {'show_delete': 1, 'is_recurring': is_recurring},
			success: function(data){
				$('div#modalcontent').html(data);
				var start_init = $('input#id_start_time_init').val();
				var end_init = $('input#id_end_time_init').val();

				$('select#id_end_time').val(end_init);
				$('select#id_start_time').val(start_init);

				show_modal_and_overlay();
				bind_edit_from_modal(edit_url);
				bind_delete_from_modal(delete_url);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

function bind_add_item() {
	$('button.addscheduleitem').click(function(){
		var edit_url = $(this).attr('action');
		var start_val = $(this).attr('id');
		$.ajax({
			type: 'GET',
			url: edit_url,
			data: {},
			success: function(data){
				$('div#modalcontent').html(data);
				var start_init = $('input#id_start_time_init').val();
				var end_init = $('input#id_end_time_init').val();

				$('select#id_end_time').val(end_init);
				$('select#id_start_time').val(start_init);

				show_modal_and_overlay();
				bind_edit_from_modal(edit_url);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}


function get_schedule_table(){
	// Load or refresh the schedule table div contents from ajax call
	$.ajax({
		url: $('div#get_schedule').text(),
		type: 'GET',
		success: function(data){
			$('div#schedulecontainer').html(data);
			bind_modal_open_schedule_options();
			bind_modal_close();
			init_schedule_toggled_view();
			bind_add_item();
		},
	})
}


/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
	get_schedule_table();

});
