$(function(){
  function format(x){
    if(x<10){
      return "0"+x.toString() ;
    }else{
      return x.toString() ;
    }
  }
  updateTime = function(){
    //alert("Hello");
    $(".thumbnails").children('li').each(function(){
      if($(this).children(".thumbnail").children("#discountDiv").children("#timeLeftDiv").length ){
        //console.log("flash discount detected : " + $(this).attr("product-id"))
        id = $(this).attr("product-id") ;
        timeLeft = $(this).children(".thumbnail").children("#discountDiv").children("#timeLeftDiv").children("#timeLeft").attr("secondsLeft")
        //console.log(timeLeft)
        if(timeLeft>0){
          $(this).children(".thumbnail").children("#discountDiv").children("#timeLeftDiv").children("#timeLeft").attr("secondsLeft",timeLeft-1);
          $(this).children(".thumbnail").children("#discountDiv").children("#timeLeftDiv").children("#timeLeft").html(format(Math.floor(timeLeft/3600))+":"+format(Math.floor((timeLeft%3600)/60))+":"+format((timeLeft%60)))
        }else{
          $(this).children(".thumbnail").children("#discountDiv").children("#timeLeftDiv").children("#timeLeft").attr("secondsLeft",0);
          $(this).children(".thumbnail").children("#discountDiv").children("#timeLeftDiv").children("#timeLeft").html("terminée")
        }
      }
    });
  }
  setInterval(updateTime, 1000)
});
