$( document ).ready(function(){
	$('.modal').modal();
  	$(".button-collapse").sideNav();
  	$('.collapsible').collapsible();
  	$('.materialboxed').materialbox();
  	$('select').material_select();
  	$('.datepicker').pickadate({
		selectMonths: true,
		selectYears: 1, 
		disable: [
		{from: [2000,1,1],to: true},
			2,3,4,5,6
		],
		max: true+20,
		format: 'yyyy-mm-dd',
		closeOnSelect: true
	});
})