document.addEventListener('DOMContentLoaded', function() {
  function fillSelect(sel, values) {
    if (!sel) return;
    sel.innerHTML = '';
    var opt = document.createElement('option'); opt.text = ''; opt.value = ''; sel.add(opt);
    values.forEach(function(v){ var o=document.createElement('option'); o.value=v; o.text=v; sel.add(o); });
  }

  var months = Array.from({length:12}, (_,i)=>i+1);
  var days = Array.from({length:31}, (_,i)=>i+1);
  var years = (function(){ var a=[]; for(var y=2006;y>=1941;y--) a.push(y); return a; })();

  fillSelect(document.querySelector('select[name="month"]'), months);
  fillSelect(document.querySelector('select[name="day"]'), days);
  fillSelect(document.querySelector('select[name="year"]'), years);

  var agree = document.getElementById('agree');
  var submit = document.querySelector('.btn-joy.btn-lg');
  if (agree && submit) {
    submit.disabled = !agree.checked;
    agree.addEventListener('change', function(){ submit.disabled = !agree.checked; });
  }
});
