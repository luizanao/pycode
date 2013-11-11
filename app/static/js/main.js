$(document).ready(function() {
  
  $("#print").on("click",function(){
      window.print();
  });


  $("#download-pdf").on("click",function(){
      var content = $('pre').html();
      //console.log(content);
      $.post("/makepdf", {  content: content } );
  });
  

});

$(document).delegate('#code', 'keydown', function(e) {
  var keyCode = e.keyCode || e.which;

  if (keyCode == 9) {
    e.preventDefault();
    var start = $(this).get(0).selectionStart;
    var end = $(this).get(0).selectionEnd;

    // set textarea value to: text before caret + tab + text after caret
    $(this).val($(this).val().substring(0, start)
                + "\t"
                + $(this).val().substring(end));

    // put caret at right position again
    $(this).get(0).selectionStart =
    $(this).get(0).selectionEnd = start + 1;
  }
});

