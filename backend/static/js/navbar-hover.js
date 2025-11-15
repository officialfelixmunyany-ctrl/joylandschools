// Enable keyboard-accessible hover behavior for Bootstrap dropdowns on non-touch devices
(function(){
  function isTouch() { return ('ontouchstart' in window) || navigator.maxTouchPoints > 0; }
  if (isTouch()) return; // don't enable hover on touch devices

  document.querySelectorAll('.navbar .dropdown').forEach(function(drop){
    drop.addEventListener('mouseenter', function(){
      drop.classList.add('show');
      var menu = drop.querySelector('.dropdown-menu');
      if(menu) {
        menu.classList.add('show');
      }
    });
    drop.addEventListener('mouseleave', function(){
      drop.classList.remove('show');
      var menu = drop.querySelector('.dropdown-menu');
      if(menu) {
        menu.classList.remove('show');
      }
    });
    // ensure focus/blur still works for keyboard users
    drop.addEventListener('focusin', function(){ drop.classList.add('show'); var m=drop.querySelector('.dropdown-menu'); if(m) m.classList.add('show'); });
    drop.addEventListener('focusout', function(){ drop.classList.remove('show'); var m=drop.querySelector('.dropdown-menu'); if(m) m.classList.remove('show'); });
  });
})();
