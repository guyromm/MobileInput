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
	  var excl = el.target.className.split(' ').indexOf('exclusive')!=-1;
	  var defmethod = el.target.className.split(' ').indexOf('defmethod')!=-1;
	  if (excl)
	  {
	      var sval = $(el.target).text()
	  }
	  else
	  {
	      var sval = $('#'+tn).val()+($('#'+tn).val().length?', ':'')+$(el.target).text();
	  }

	  $('#'+tn).val(sval);
	  if (defmethod)
	  {
	      var toset = def_methods[sval];
	      console.log('setting method to %o (%o)',toset,tn);
	      $('#method').val(toset);
	  }
      });
      $('#now_lnk').bind('click',function(el) {
	  var d = new Date();
	  $('#when').val(ISODateString(d));
      });
  });
