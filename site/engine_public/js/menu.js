// 'use strict';

// (function() {
//   var body = document.body;
//   var burgerMenu = document.getElementsByClassName('b-menu')[0];
//   var burgerContain = document.getElementsByClassName('b-container')[0];
//   var burgerNav = document.getElementsByClassName('b-nav')[0];

//   burgerMenu.addEventListener('click', function toggleClasses() {
//     [body, burgerContain, burgerNav].forEach(function (el) {
//       el.classList.toggle('open');
//     });
//   }, false);
// })();

(function() {
	$('.js-nav-toggle').on('click', function(event){
		event.preventDefault();
		var $this = $(this);
		console.log('qwe')
		if ($('body').hasClass('offcanvas')) {
			$this.removeClass('active');
			$('body').removeClass('offcanvas');	
		} else {
			$this.addClass('active');
			$('body').addClass('offcanvas');	
		}
	});

})();

