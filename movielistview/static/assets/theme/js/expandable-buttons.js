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
  $("#"+id+".form-container-expandable").find('.search-wrapper').removeClass('focused');
  $('.search-wrapper').find('.fa-minus-circle').addClass('hide');
  $('.search-wrapper').find('.fa-search').removeClass('hide');
  $('.search-wrapper').find('.search-input').val('');

  $("#"+id+".form-container-expandable").find('input[type=submit]').removeClass('exit');
  $("#"+id+".form-container-expandable").find('input[type=submit]').val('Search');
  $("#"+id+".form-container-expandable").find('.input.cancel').removeClass('exit');
}


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
