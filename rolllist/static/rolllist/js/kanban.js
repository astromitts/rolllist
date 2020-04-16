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

function kanban_bind_delete_from_modal(delete_url){
	$('form#kanban_delete').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: delete_url,
			data: $(this).serialize(),
			success: function(data){
				get_todo_table();
				hide_modal_and_overlay();
			},
			error: function(data){
				alert("there was an error");
				hide_modal_and_overlay();
			}
		});
	});
}

function kanban_bind_edit_from_modal(edit_url){
	$('form#kanban_edit').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			url: edit_url,
			data: $(this).serialize(),
			success: function(data){
				get_todo_table();
				hide_modal_and_overlay();
			},
			error: function(data){
				alert("there was an error");
				hide_modal_and_overlay();
			}
		});
	});
}

function bind_modal_kanban_edit(){
	// Handle the modal opening function for the to-do view
	$('span.js-edit-kanbanitem').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('data-edit-url');
		var delete_url = $(this).attr('data-delete-url');
		$.ajax({
			type: 'GET',
			url: target_url,
			data: {'show_delete': true},
			success: function(data){
				$('div#modalcontent').html(data);
				show_modal_and_overlay();
				kanban_bind_edit_from_modal(target_url);
				kanban_bind_delete_from_modal(delete_url);
			},
			error: function(data){
				alert("there was an error");
			}
		});
	});
}

function bind_modal_kanban_add(){
	$('a.js-add-kanban').click(function(event){
		event.preventDefault();
		var target_url = $(this).attr('href');
		$.ajax({
			type: 'GET',
			url: target_url,
			data: {},
			success: function(data){
				$('div#modalcontent').html(data);
				show_modal_and_overlay();
				kanban_bind_edit_from_modal(target_url);
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
			bind_modal_kanban_edit();
			bind_todo_generic_handlers();
			bind_modal_close();
			bind_toggle_kanban_links();
		},
	})
}

$(document).ready(function(){
	get_todo_table();
	bind_modal_kanban_add();
});