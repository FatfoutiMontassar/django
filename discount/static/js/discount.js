$(function(){

  var d = new Date();
  var n = d.getTimezoneOffset();
  $("#timeOffset").attr('value',n)
  //alert(n);
  $(".list-group-item").click(function(){
    // this function will change the state of a product from non selected to selected ..
    // and the reverse operation
    id = $(this).attr('product-id') ;
    //alert("clicked .." + id)

    if($(this).hasClass('active')){
      $(this).removeClass();
      $(this).addClass('list-group-item').addClass('product') ;
    }else{
      $(this).addClass('active') ;
    }

  });

  $("#preSubmit").click(function(){
    var selectedProducts = ""
    $("#list-of-selected-products").children('a').each(function(){
      if($(this).hasClass('active')){
        product_id = $(this).attr("product-id")
        selectedProducts += (product_id + "&")
      }
    });
    $("#form").append('<input type="hidden" name="relatedProducts" id="relatedProducts" value="' + selectedProducts + '">')
    //alert(selectedProducts) ;

    var selectedCollections = ""
    $("#list-of-selected-collections").children('a').each(function(){
      if($(this).hasClass('active')){
        collection_id = $(this).attr("collection-id")
        selectedCollections += (collection_id + "&")
      }
    });
    $("#form").append('<input type="hidden" name="relatedCollections" id="relatedCollections" value="' + selectedCollections + '">')

    $("#form").submit()
  });
  function fun(str1,str2){
    for(var i = 0 ; i <= str1.length-str2.length ; i++){
      var ret = true
      for(var j = 0 ; j < str2.length ; j++){
        if(str1[i+j] != str2[j]){
          ret = false
          break
        }
      }
      if(ret == true)return true
    }
    return false
  }
  $("#choose-list-search-products").keyup(function(){
    if($("#choose-list-search-products").val() != "" ){
      var input = $("#choose-list-search-products").val()
      $("#list-of-selected-products").children('a').each(function(){
        $(this).css('display','')
      });
      $("#list-of-selected-products").children('a').each(function(){
        product_name = $(this).attr("product-name")
        if(!fun(product_name.toLowerCase(),input.toLowerCase()) && !fun(input.toLowerCase(),product_name.toLowerCase()) && !$(this).hasClass('active') ){
          //alert(product_name + "1")
          $(this).css('display','none')
        }else{
          //alert(product_name + "2")
        }
      });
    }else{
      $("#list-of-selected-products").children('a').each(function(){
        $(this).css('display','')
      });
    }
  });
  $("#choose-list-search-collections").keyup(function(){
    if($("#choose-list-search-collections").val() != "" ){
      var input = $("#choose-list-search-collections").val()
      $("#list-of-selected-collections").children('a').each(function(){
        $(this).css('display','')
      });
      $("#list-of-selected-collections").children('a').each(function(){
        collection_name = $(this).attr("collection-name")
        if(!fun(collection_name.toLowerCase(),input.toLowerCase()) && !fun(input.toLowerCase(),collection_name.toLowerCase()) && !$(this).hasClass('active') ){
          //alert(product_name + "1")
          $(this).css('display','none')
        }else{
          //alert(product_name + "2")
        }
      });
    }else{
      $("#list-of-selected-collections").children('a').each(function(){
        $(this).css('display','')
      });
    }
  });

});
