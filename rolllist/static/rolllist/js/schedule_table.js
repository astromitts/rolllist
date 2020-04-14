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
	$('button.item-expand').click(function(){
		var $targetSpan = $('span#item-full-' + $(this).attr('id'));
		var $buttonSpan = $('div#item-actions-' + $(this).attr('id'));
		if ( $targetSpan.is(':visible')) {
			$targetSpan.hide();
			$buttonSpan.hide();
		} else {
			$targetSpan.show();
			$buttonSpan.show();
		}
		
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
			bind_schedule_controls();
			bind_add_item();
			init_schedule_display();
		},
	})
}


/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
	get_schedule_table();

});
