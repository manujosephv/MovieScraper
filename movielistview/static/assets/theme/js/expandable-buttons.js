//Expandable buttons
bindFormClickInit();
//init the form
function bindFormClickInit(){  
  $('.form-container-expandable').on('click', function(e) {
    e.preventDefault();
    if ( !$( this ).hasClass( "disabled" ) ) {
    var id = $(this).prop('id');
      $("#"+id+".form-container-expandable").attr('style','z-index:1002;');
    toggleForm(id);
    //Ensure container doesn't togleForm when open
//    $(this).off();
      $("#"+id+".form-container-expandable").off();
    }
  });
}

//Opening the form
function bindFormClick(id){
  $("#"+id+".form-container-expandable").on('click', function(e) {
    e.preventDefault();
    if ( !$( this ).hasClass( "disabled" ) ) {
    var id = $(this).prop('id');
    $("#"+id+".form-container-expandable").attr('style','z-index:1002;');
    toggleForm(id);
      
    //Ensure container doesn't togleForm when open
//    $(this).off();
      $("#"+id+".form-container-expandable").off();
    }
  });
}

//Closing the form
$('#form-close, .form-overlay').click(function(e) {
  e.stopPropagation();
  e.preventDefault();
  var id = $(this).closest("div").prop("id");
    toggleForm(id);
    setTimeout(
  function() 
  {
    //do something special
      $("#"+id+".form-container-expandable").attr('style','z-index:1000;');
  }, 500);
    
  bindFormClick(id);
});

function toggleForm(id){
  $("#"+id+".form-container-expandable").toggleClass('expand');
  $("#"+id+".form-container-expandable").children().toggleClass('expand');
  $('body').toggleClass('show-form-overlay');
  $('.form-submitted').removeClass('form-submitted');
}

////Form validation
//$('form').submit(function() {
//  var form = $(this);
//  form.find('.form-error').removeClass('form-error');
//  var formError = false;
//  
//  form.find('.input').each(function() {
//    if ($(this).val() == '') {
//      $(this).addClass('form-error');
//      $(this).select();
//      formError = true;
//      return false;
//    }
//    else if ($(this).hasClass('email') && !isValidEmail($(this).val())) {
//      $(this).addClass('form-error');
//      $(this).select();
//      formError = true;
//      return false;
//    }
//  });
//  
//  if (!formError) {
//    $('body').addClass('form-submitted');
//    $('#form-head').addClass('form-submitted'); 
//    setTimeout(function(){
//      $(form).trigger("reset");
//    }, 1000);
//  }
//  return false;
//});
//
//function isValidEmail(email) {
//    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
//    return pattern.test(email);
//};

//Form inside

        $('.search-wrapper').find('.fa-search').on('click', function(){
            var id = $(this).parent('.search-wrapper').prop('id');
            console.log(id + "clicked") ;
            $('#'+id+'.search-wrapper').addClass('focused')
            $('#'+id+'.search-wrapper').find('.fa-search').addClass('hide')
            $('#'+id+'.search-wrapper').find('.fa-minus-circle').removeClass('hide')
//            $('#'+id+'.search-wrapper').find('.fa-search').toggleClass('fa-search','fa-close');
        });
        
        $('.search-wrapper').find('.fa-minus-circle').on('click',function(){
            if (!$(this).hasClass('hide')){
                    $(this).parent('.search-wrapper').removeClass('focused');
                    $(this).addClass('hide');
                    $(this).siblings('.fa-search').removeClass('hide')
                    $(this).siblings('.search-input').val('');
            }
        });
