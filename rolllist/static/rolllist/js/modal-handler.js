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
				reload_function();
				hide_modal_and_overlay();
			},
			error: function(data){
				hide_modal_and_overlay();
				alert("there was an error");
			}
		});
	});
}