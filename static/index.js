function ISODateString(d){
    function pad(n){return n<10 ? '0'+n : n}
    return d.getUTCFullYear()+'-'
	+ pad(d.getUTCMonth()+1)+'-'
	+ pad(d.getUTCDate())+'T'
	+ pad(d.getUTCHours())+':'
	+ pad(d.getUTCMinutes())
	//+':'+ pad(d.getUTCSeconds())
	+'Z'}

  $(function() {
      $('.set').bind('click',function(el) {
	  el.preventDefault();

	  //extract our secondary class
	  var tn = el.target.className.split(' ')[1];
	  var excl = el.target.className.split(' ')[2];
	  if (excl)
	      $('#'+tn).val($(el.target).text());
	  else
	      $('#'+tn).val($('#'+tn).val()+($('#'+tn).val().length?', ':'')+$(el.target).text());
      });

      $('#now_lnk').bind('click',function(el) {
	  var d = new Date();
	  $('#when').val(ISODateString(d));
      });

      $('#amt').focus();
  });
