// AJAX for posting
function scrape_movies() {
    console.log("create post is working!") // sanity check
    console.log($('#scrape_movies_form').serialize())
    var frm = $('#scrape_movies_form');
    var frm_results = $('#form_results')
    if (!frm_results.hasClass("hidden")){
        frm_results.toggleClass('hidden');
    }
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
            frm_results.html("<span>You have " + json.no_of_rows +" movies to review</span><br><a href = '/view_movies/'> View Them Now </a>");
            if (frm_results.hasClass("hidden")){
                frm_results.toggleClass('hidden');
            }
            if (frm_results.hasClass("alert-danger")){
                frm_results.addClass("alert-success").removeClass("alert-danger");
            }
            
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              //  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //frm.LoadingOverlay("hide");
            frm_results.html("<span>Something went wrong. Try again</span>");
            if (frm_results.hasClass("hidden")){
                frm_results.toggleClass('hidden');
            }
            if (frm_results.hasClass("alert-success")){
                frm_results.addClass("alert-danger").removeClass("alert-success");
            }
        }
    });
};

function mark_read_movies(clicked_id) {
    console.log("mark read is working!") // sanity check
    // console.log($('#mark-read-movies-form').serialize())
    console.log(clicked_id)
    data_dict = {'post_id':clicked_id}
    // var frm = $('#mark-read-movies-form');
    $.ajax({
        type: 'POST', //GET or POST as defined in HTML
            url: '/mark_read_movies/', //action defined in HTML
            data: {post_id , clicked_id},
            dataType : "json",

        // handle a successful response
        success : function(json) {
            frm[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
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


