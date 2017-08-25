$(function(){

  $("#uploadCollectionImage").click(function(){
    $("#collectionImageInput").click() ;
  });

  function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#previewImage').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
  }

  $("#collectionImageInput").change(function(){
      readURL(this);
  });

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

  $("#preSubmitButton").click(function(){
    var selectedProducts = ""
    $("#list-of-selected-products").children('a').each(function(){
      if($(this).hasClass('active')){
        product_id = $(this).attr("product-id")
        selectedProducts += (product_id + "&")
      }
    });
    $("#form").append('<input type="hidden" name="relatedProducts" id="relatedProducts" value="' + selectedProducts + '">')
    //alert(selectedProducts) ;
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
  $("#choose-list-search").keyup(function(){
    if($("#choose-list-search").val() != "" ){
      var input = $("#choose-list-search").val()
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


  // this code is responsible on the deletion of collection

});

function deleteCollection(id){
		var ans = confirm("Are you sure that you want to delete this Collection!!")
		if(ans == true){
			window.location = "/collections/deleteCollection/"+id+"/";
		}
}
