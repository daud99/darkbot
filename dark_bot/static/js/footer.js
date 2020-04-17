$(document).ready(function(){

    $('#custmenu').click(function()
{console.log("hello");
	if ($(window).width() < 768)
	{
	 if ($(".ari1").css('display').toLowerCase() == 'block')
	 {
		$('.ari1').css('display','none');
	 }
	 else
	 {
			 $(".ari1").css('display', 'block');
	 }
	}
});
$('#company_menu').click(function()
{
	if ($(window).width() < 768)
	{
	 if ($(".ari2").css('display').toLowerCase() == 'block')
	 {
		$('.ari2').css('display','none');
	 }
	 else
	 {
			 $(".ari2").css('display', 'block');
	 }
	}
});
$('#find_menu').click(function()
{
	if ($(window).width() < 768)
	{
	 if ($(".ari3").css('display').toLowerCase() == 'block')
	 {
		$('.ari3').css('display','none');
	 }
	 else
	 {
			 $(".ari3").css('display', 'block');
	 }
	}
});
$('#email_menu').click(function()
{
	if ($(window).width() < 768)
	{
	 if ($(".ari4").css('display').toLowerCase() == 'block')
	 {
		$('.ari4').css('display','none');
		$('.line4').css('display','block');
	 }
	 else
	 {
			 $(".ari4").css('display', 'block');
			 $('.line4').css('display','none');
	 }
	}
});
function checkWidth(init)
{
	if ($(window).width() < 768)
	{
	 $('.ari1,.ari2,.ari3,.ari4').css('display','none');
	 $('.ungli').css('color','black');
	 $('.list').addClass('list-group');
	 $('.ungli').addClass('list-group-item list-group-item-action');
	 $('h5').addClass('angotha');
	 $('.line').css('display','block');
	}
	else if ($(window).width() > 768)
	{
		$('.ari1,.ari2,.ari3,.ari4').css('display','block');
		$('.ungli').css('color','white');
		$('.list').removeClass('list-group');
		$('.ungli').removeClass('list-group-item list-group-item-action');
		$('h5').removeClass('angotha');
		$('.line').css('display','none');
	}
}

    checkWidth(true);

	$(window).resize(function() {
		checkWidth(true);
	});
});



