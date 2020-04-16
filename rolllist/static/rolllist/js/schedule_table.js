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

function schedule_toggled_view(show_target_button){ // i.e. "expand"

	var selected_target_id = show_target_button.attr('id'); // i.e. table-toggled-view_full
	var deselected_target_id = show_target_button.attr('data-hide-div'); // i.e. table-toggled-view_collapsed
	
	var new_visible_button_id = deselected_target_id;
	var new_visible_button = $('button#' + new_visible_button_id);

	var selected_target_div = $('div.' + selected_target_id);
	var deselected_target_div = $('div.' + deselected_target_id);
	
	
	selected_target_div.show();
	show_target_button.hide();

	deselected_target_div.hide();
	new_visible_button.show();

	Cookies.set('_rollist-schedule-view', selected_target_id);
}

function bind_schedule_toggle_to_buttons() {
	$('button.js-schedule-toggle').click(function(){
		schedule_toggled_view($(this));
	});
}

function init_schedule_toggled_view() {
	valid_toggle_options = ['table-toggled-view_full', 'table-toggled-view_collapsed'];
	var show_button_id = Cookies.get('_rollist-schedule-view');
	if ($.inArray(show_button_id, valid_toggle_options) < 0) {
		show_button_id = valid_toggle_options[0];
	}
	var show_button = $('button#' + show_button_id);
	schedule_toggled_view(show_button);
	bind_schedule_toggle_to_buttons();
}


// ##############  END display style of the schedule table ##########


/* SCHEDULE VIEW HANDLERS */
function schedule_bind_delete_from_modal(delete_url){
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

function schedule_bind_edit_from_modal(edit_url){
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

		var start_val = $(this).attr('id');
		$.ajax({
			type: 'GET',
			url: edit_url,
			data: {'show_delete': 1},
			success: function(data){
				$('div#modalcontent').html(data);
				var start_init = $('input#id_start_time_init').val();
				var end_init = $('input#id_end_time_init').val();

				$('select#id_end_time').val(end_init);
				$('select#id_start_time').val(start_init);

				show_modal_and_overlay();
				schedule_bind_edit_from_modal(edit_url);
				schedule_bind_delete_from_modal(delete_url);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

function schedule_bind_add_item() {
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

				schedule_bind_edit_from_modal(edit_url);
				show_modal_and_overlay();
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
			schedule_bind_add_item();
		},
	})
}


/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
	get_schedule_table();

});
