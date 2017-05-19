// AJAX for posting
function scrape_movies() {
    console.log("create post is working!") // sanity check
    console.log($('#scrape_movies_form').serialize())
    var frm = $('#scrape_movies_form');
    var frm_results = $('#form_results')
    //frm.LoadingOverlay("show");
    $.ajax({
        type: frm.attr('method'), //GET or POST as defined in HTML
            url: frm.attr('action'), //action defined in HTML
            data: frm.serialize(), //Serializing the object to pass through

        // handle a successful response
        success : function(json) {
            frm[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
            //frm.LoadingOverlay("hide", true);
            frm_results.html("<span>You have " + json.no_of_rows +" movies to review</span><br><a href = ''> View Them Now </a>");
            frm_results.toggleClass('hidden');
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              //  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

