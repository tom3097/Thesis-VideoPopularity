/*
 * Slider for sample prediction results.
 */

$(document).ready(function() {
    var images = $('#main-slider img');

    for (var i = 0; i < images.length; i++) {
    	if (i === 0) {
    		$('#main-slider img').eq(i).addClass('current 1');
    	} else {
    		$('#main-slider img').eq(i).addClass(i);
    	}
    }

    setInterval(function(){moveImg()}, 3000);
});
	
function moveImg(){
	var oCurPhoto = $('#main-slider img.current');
	var oNxtPhoto = oCurPhoto.next();

	if (oNxtPhoto.length == 0) {
		oNxtPhoto = $('#main-slider img:first');
	}
	
	oCurPhoto.removeClass('current').addClass('previous');
	oNxtPhoto.css({opacity: 0.0}).addClass('current').animate({opacity: 1.0}, 1000,
		function(){
			oCurPhoto.removeClass('previous');
		});
}
