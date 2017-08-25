/*
  add new sent messages without reloading the page
*/
$(function () {
  var scrolled = 0
  function add_new_messages() {
    var to   = $("#picture-upload-form input[name=to]").val();
    var csrf = $("#list-of-messages").attr("csrf")
    //alert(to)
    $.ajax({
        url: '/messenger/add_new_messages/',
      data:{
        'username':to,
        'csrfmiddlewaretoken': csrf,
      },
      cache: false,
      type:'post',
      success: function (data) {
        if(data.length > 0){
          $("#list-of-messages").append(data);
          var numberOfMessages = $("#list-of-messages").attr("numberOfMessages");
          document.getElementById("list-of-messages").setAttribute("numberOfMessages",(parseInt(numberOfMessages) + 1));

          scrolled=scrolled+10000;
          $("#list-of-messages").animate({
            scrollTop:  scrolled
          });
        }
      },
      complete: function () {
        window.setTimeout(add_new_messages, 10000);
      }
    });
  };
  add_new_messages();
});
