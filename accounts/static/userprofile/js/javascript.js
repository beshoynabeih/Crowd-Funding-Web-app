
  

$(function(){

  setTimeout(function() {
    $('#message').fadeOut('slow');
  }, 1000);


  $('#info_link').click()


  $('input').blur(function(){
       element=$(this)
    if(element.attr("type") == "text")
  {
      if(!$(this).val())
          ($(this).addClass("is-invalid"))
      else
      ($(this).removeClass("is-invalid"))
  }
  else if(element.attr("type") == "number")
  {
      if($(this).val()<=0)
          ($(this).addClass("is-invalid"))
      else
      ($(this).removeClass("is-invalid"))
  }
  })


  $('select').blur(function(){
    if($(this).val()< 1 )
        ($(this).addClass("is-invalid"))
    else
      ($(this).removeClass("is-invalid"))})

    $('textarea').blur(function(){
    if(!$(this).val())
      ($(this).addClass("is-invalid"))
    else
      ($(this).removeClass("is-invalid"))})


    $('input[type="date"]').change(function(){
      console.log("dnnnnnnnnnnnnnnfn")
         if($(this).attr('name') == 'start_date')
      {
        start_date=parseDMY($(this).val())
        end_date=parseDMY($(this).next().val())

        console.log(start_date)
        console.log(end_date)

        if($(this).val() > $(this).next().val())
          $(this).addClass("is-invalid")
      }
      else if($(this).attr('name') == 'end_date')
      {
        end_date=parseDMY($(this).val())
        start_date=parseDMY($(this).prev().val())
        console.log(start_date)
        console.log(end_date)
          if($(this).val() < $(this).next().val())
                $(this).addClass("is-invalid")
      }
    })


})

function validation(form_id)
{
  vaild=true
  $($('#'+form_id).prop('elements')).each(function(){

    if ($(this).hasClass('is-invalid'))
        vaild=false
})
  if(vaild)
    $("#"+form_id).submit();
}




function parseDMY(value) {
  var date = value.split("-");
  var d = parseInt(date[0], 10),
      m = parseInt(date[1], 10),
      y = parseInt(date[2], 10);
  return new Date(y, m - 1, d);
}
    

