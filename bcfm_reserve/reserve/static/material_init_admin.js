$( document ).ready(function(){
	$('.modal').modal();
  	$(".button-collapse").sideNav();
  	$('.collapsible').collapsible();
  	$('.materialboxed').materialbox();
  	$('select').material_select();
  	$('.datepicker').pickadate({
		selectMonths: true,
		selectYears: 1, 
		format: 'yyyy-mm-dd',
		closeOnSelect: true
	});
})