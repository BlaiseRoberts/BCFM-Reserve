$( document ).ready(function(){
	$('.modal').modal();
  	$(".button-collapse").sideNav();
  	$('.collapsible').collapsible();
  	$('.materialboxed').materialbox();
  	$('.datepicker').pickadate({
		selectMonths: true,
		selectYears: 1, 
		disable: [
			2,3,4,5,6
		],
		min: true,
		format: 'yyyy-mm-dd',
		closeOnSelect: true
	});
})