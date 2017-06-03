// AJAX for posting
function scrape_movies() {
    console.log("create post is working!") // sanity check
    console.log($('#scrape_movies_form').serialize())
    var frm = $('#scrape_movies_form');
    var frm_results_title = $('#form-results-title')
    var frm_results_text = $('#form-results-text')
    $.ajax({
        type: frm.attr('method'), //GET or POST as defined in HTML
            url: frm.attr('action'), //action defined in HTML
            data: frm.serialize(), //Serializing the object to pass through

        // handle a successful response
        success : function(json) {
            frm[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
            //frm.LoadingOverlay("hide", true);
            
            // frm_results_title.html("<span>Scrape Complete</span>");
            // frm_results_text.html("<span>" + json.movie_count_added +" movies added</span><br><a style='color:#fff;font-size:small;' href = '/view_movies/'> View Them Now </a>");
            // $('#popup-box').css('background-color', '#16b766');
            // $('.popup-wrap').fadeIn(250);
            // $('.popup-box').removeClass('transform-out').addClass('transform-in');
            // $('#last_scrap_time').html("Last scrape done on " + humanizeDate(json.last_scrap_time))
            console.log("started");
            show_notifications('notification_scrape_start',3000) // another sanity check
            var poll_xhr;
            var willstop = 0;
            (function(){
                var poll = function(){
                  var json_dump = json.data;
                  var task_id = json.task_id;

                  console.log(task_id);
                  poll_xhr = $.ajax({
                    url:'/poll_state/',
                    type: 'POST',
                    data: {
                        task_id: task_id,

                    },
                    success: function(response) {
                                console.log(response);
                                if (response.state == 'SUCCESS'){
                                    willstop = 1
                                    $('#notification_scrape_result').find('.notification-text').find('span').html('&nbsp;&nbsp;Scrape complete. ' +response.movie_count_added +' movies added');
                                    $('#last_scrape_time').html("Last scrape done on " + humanizeDate(response.last_scrape_time))
                                    show_notifications('notification_scrape_result', 5000)
                                    $('#scrap_button').removeClass('disabled')
                                    // $('#notification_scrape_result').toggleClass('hide')
                                    // setTimeout(function() {
                                    //  $('#notification_scrape_result').animate({
                                    //     top: "60%",
                                    //     opacity: 0
                                    //  }, "fast")
                                    // }, 5000);
                                }
                                }
                  });
                };

                var refreshIntervalId = setInterval(function() {
                    console.log("calling poll")
                  if(willstop == 1){
                    console.log("clearing interval")
                    clearInterval(refreshIntervalId);
                  } else{
                    poll();
                  }

                  
                },5000);
              })();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
              //  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //frm.LoadingOverlay("hide");
            $('#scrap_button').removeClass('disabled')
            frm_results_title.html("Scrape Cancelled");
            frm_results_text.html("<span>Something went wrong. Please try again.");
            $('#popup-box').css('background-color', '#ba2b1c');
            // frm_results_text.css('color','ffffff')
            $('.popup-wrap').fadeIn(250);
            $('.popup-box').removeClass('transform-out').addClass('transform-in');
        }
    });
};

function show_notifications(div_id, duration) {
    $('#' + div_id).toggleClass('hide')
    setTimeout(function() {
     $('#' + div_id).animate({
        top: "60%",
        opacity: 0
     }, "fast")
    }, duration);
}

function mark_read_movies() {
    
    var frm = $('#mark_read_form');
    $.ajax({
        type: frm.attr('method'), //GET or POST as defined in HTML
        url: frm.attr('action'), //action defined in HTML
        data: frm.serialize(), //Serializing the object to pass through
        // handle a successful response
        success : function(json) {
            // frm[0].reset(); // remove the value from the input
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

function humanizeDate(date_str) {
    var readable = new Date(date_str);  // When we pass the ISO format to the JS Date constructor, the return is "Fri Jul 04 2014 21:06:08 GMT-0400 (Eastern Daylight Time)"
    var m = readable.getMonth();  // returns 6 (note that this number is one less than the number of the month in isoformat)
    var d = readable.getDate();  // returns 15
    var y = readable.getFullYear();  // returns 2012
    var hours = readable.getHours();
    var minutes = readable.getMinutes();
    var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    // we define an array of the months in a year
    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    // we get the text name of the month by using the value of m to find the corresponding month name
    var mlong = months[m];

  return mlong + " " + d + ", " + y + ", " + strTime;
};
