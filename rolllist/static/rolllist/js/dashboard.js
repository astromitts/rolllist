function toggle_view(showdiv, hidediv) {
	$('#' + showdiv).show();
	$('#' + hidediv).hide();

	$('a#link-' + showdiv).removeClass('inactive');
	$('a#link-' + showdiv).addClass('active');
	
	$('a#link-' + hidediv).addClass('inactive');
	$('a#link-' + hidediv).removeClass('active');

	Cookies.set("_rollist-dash-show", showdiv);
	Cookies.set("_rollist-dash-hide", hidediv);
}

function init_view_toggle () {
	var showdiv = Cookies.get("_rollist-dash-show");
	var hidediv = Cookies.get("_rollist-dash-hide");
	if (showdiv == undefined) {
		showdiv = 'schedulecontainer-wrapper';
		hidediv = 'todocontainter-wrapper';
	}
	toggle_view(showdiv, hidediv);
	$('div.view-toggle a').click(function(event){
		event.preventDefault();
		var showdiv = $(this).attr('data-show-div');
		var hidediv = $(this).attr('data-hide-div');
		toggle_view(showdiv, hidediv);
	});
}

/* DOC HANDLER */
$(document).ready(function(){
	var datestr = $('div#datestr').text();
	init_view_toggle();
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