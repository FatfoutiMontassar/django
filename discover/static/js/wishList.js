$(function(){
  $(".addProductToWishList").click(function(){
    //alert("add to favorite ...");
    var span = $(this).closest(".span3") ;
    var csrf = span.attr("csrf") ;
    //alert("add " + span.attr("product-id") + " to wish list")

    $.ajax({
      url: '/discover/addToWishList/',
      data: {
        'id':span.attr("product-id"),
        'type':"P",
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        if(data == "added"){
          //alert("added")
          $(".addProductToWishList", span).addClass('active')
        }else{
          //alert("removed")
          $(".addProductToWishList", span).removeClass().addClass('addProductToWishList')
        }
      }
    });
  });

  $(".addCollectionToWishlist").click(function(){
    //alert("add collection to favorite ...");
    var span = $(this).closest(".span3") ;
    var csrf = span.attr("csrf") ;
    //alert("add " + span.attr("product-id") + " to wish list")

    $.ajax({
      url: '/discover/addToWishList/',
      data: {
        'id':span.attr("collection-id"),
        'type':"C",
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        if(data == "added"){
          //alert("added")
          $(".addCollectionToWishlist", span).addClass('active')
        }else{
          //alert("removed")
          $(".addCollectionToWishlist", span).removeClass().addClass('addCollectionToWishlist')
        }
      }
    });
  });
});
