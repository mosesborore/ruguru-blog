	/* preloader */

	const ssPreloader = function () {

	  const preloader = document.querySelector('#preloader');
	  if (!preloader) return;

	  document.querySelector('html').classList.add('ss-preload');

	  window.addEventListener('load', function () {

	    document.querySelector('html').classList.remove('ss-preload');
	    document.querySelector('html').classList.add('ss-loaded');

	    preloader.addEventListener('transitionend', function (e) {
	      if (e.target.matches("#preloader")) {
	        this.style.display = 'none';
	      }
	    });
	  });

	  // force page scroll position to top at page refresh
	  // window.addEventListener('beforeunload' , function () {
	  //     window.scrollTo(0, 0);
	  // });

	}; // end ssPreloader

	ssPreloader()