// AJAX for posting
function scrape_movies() {
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
            console.log("started");
            show_notifications('notification_scrape_start',3000) // another sanity check
            var poll_xhr;
            var willstop = 0;
            (function(){
                var poll = function(){
                  var json_dump = json.data;
                  var task_id_scrape = json.task_id_scrape;

                  console.log(task_id_scrape);
                  poll_xhr = $.ajax({
                    url:'/poll_state_scrape/',
                    type: 'POST',
                    data: {
                        task_id_scrape: task_id_scrape,

                    },
                    success: function(response) {
                                console.log(response);
                                if (response.state == 'SUCCESS'){
                                    willstop = 1
                                    $('#notification_scrape_result').find('.notification-text').find('span').html('&nbsp;&nbsp;Scrape complete. ' +response.movie_count_added +' movies added');
                                    $('#last_scrape_time').html("Last scrape done on " + humanizeDate(response.last_scrape_time))
                                    show_notifications('notification_scrape_result', 5000)
                                    enable_buttons();
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
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            enable_buttons();
            frm_results_title.html("Scrape Cancelled");
            frm_results_text.html("<span>Something went wrong. Please try again.");
            $('#popup-box').css('background-color', '#ba2b1c');
            $('.popup-wrap').fadeIn(250);
            $('.popup-box').removeClass('transform-out').addClass('transform-in');
        }
    });
};

function update_ratings() {
    
    var frm_results_title = $('#form-results-title')
    var frm_results_text = $('#form-results-text')
    $.ajax({
        type: 'GET', //GET or POST as defined in HTML
            url: '/update_ratings/', //action defined in HTML

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("started");
            show_notifications('notification_ratings_start',3000) // another sanity check
            var poll_xhr;
            var willstop = 0;
            (function(){
                var poll = function(){
                  var json_dump = json.data;
                  var task_id_rating = json.task_id_rating;

                  console.log(task_id_rating);
                  poll_xhr = $.ajax({
                    url:'/poll_state_rating/',
                    type: 'POST',
                    data: {
                        task_id_rating: task_id_rating,

                    },
                    success: function(response) {
                                console.log(response);
                                if (response.state == 'SUCCESS'){
                                    willstop = 1
                                    $('#notification_ratings_result').find('.notification-text').find('span').html('&nbsp;&nbsp;Update complete. ' +response.movie_rating_updated +' movies updated');
                                    show_notifications('notification_ratings_result', 5000)
                                    enable_buttons();
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
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            enable_buttons();
            frm_results_title.html("Update Cancelled");
            frm_results_text.html("<span>Something went wrong. Please try again.");
            $('#popup-box').css('background-color', '#ba2b1c');
            $('.popup-wrap').fadeIn(250);
            $('.popup-box').removeClass('transform-out').addClass('transform-in');
        }
    });
};


function remove_duplicates() {
    
    var frm_results_title = $('#form-results-title')
    var frm_results_text = $('#form-results-text')
    $.ajax({
        type: 'GET', //GET or POST as defined in HTML
            url: '/remove_duplicates/', //action defined in HTML

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("started");
            show_notifications('notification_duplicates_start',3000) // another sanity check
            var poll_xhr;
            var willstop = 0;
            (function(){
                var poll = function(){
                  var json_dump = json.data;
                  var task_id_duplicate = json.task_id_duplicate;

                  console.log(task_id_duplicate);
                  poll_xhr = $.ajax({
                    url:'/poll_state_duplicates/',
                    type: 'POST',
                    data: {
                        task_id_duplicate: task_id_duplicate,

                    },
                    success: function(response) {
                                console.log(response);
                                if (response.state == 'SUCCESS'){
                                    willstop = 1
                                    $('#notification_duplicates_result').find('.notification-text').find('span').html('&nbsp;&nbsp;Removed '+ response.duplicates_removed +' Duplicates.');
                                    show_notifications('notification_duplicates_result', 5000)
                                    enable_buttons();
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

                  
                },4000);
              })();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            enable_buttons();
            frm_results_title.html("Remove Duplicates Cancelled");
            frm_results_text.html("<span>Something went wrong. Please try again.");
            $('#popup-box').css('background-color', '#ba2b1c');
            $('.popup-wrap').fadeIn(250);
            $('.popup-box').removeClass('transform-out').addClass('transform-in');
        }
    });
};



function show_notifications(div_id, duration) {
    $('#' + div_id).css({"top":"40%","opacity":1})
    $('#' + div_id).toggleClass('hide');
    setTimeout(function() {
     $('#' + div_id).animate({
        top: "60%",
        opacity: 0
     }, "fast")
     $('#' + div_id).toggleClass('hide');
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
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function search_movies(id) {
    console.log(id + "in search ajax fn")    
    var frm = $('#'+id);
    $.ajax({
        type: frm.attr('method'), //GET or POST as defined in HTML
        url: frm.attr('action'), //action defined in HTML
        data: frm.serialize(), //Serializing the object to pass through
        // handle a successful response
        success : function(json) {
            // frm[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            movies = json.result;
            frm.addClass('searched');
            frm.find('input[type=submit]').val('Go Ahead');
            frm.siblings('#form-head').find('h4').html(movies + " movies selected! Proceed?");
            frm.addClass('form-submitted');
            frm.siblings('#form-head').addClass('form-submitted');
            // setTimeout(function(){
            //       frm.trigger("reset");
            //     }, 1000);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            frm.addClass('searched');
            frm.find('input[type=submit]').val('Search Again').prop('disabled',true); //disable option
            frm.siblings('#form-head').find('h4').html("Something unexpected Happened. Please try again");
            frm.addClass('form-submitted');
            frm.siblings('#form-head').addClass('form-submitted');
            frm.find('input[type=submit]').addClass('form-error');
            setTimeout(function(){
              frm.find('input[type=submit]').removeClass('form-error');
            }, 1000);
            
        }
    });
};


function mark_read_bulk() {
    console.log("in mark_read_bulk ajax fn");
    // var frm = $('#'+id);
    $.ajax({
        type: 'POST', //GET or POST as defined in HTML
        url: '/mark_read_bulk/', //action defined in HTML
        // data: frm.serialize(), //Serializing the object to pass through
        // handle a successful response
        success : function(json) {
            // frm[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            movies = json.count;
            frm.siblings('#form-head').find('h4').html(movies + " movies marked read!");
            exit_form();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            frm.find('input[type=submit]').val('Try Again').prop('disabled',true); //disable option
            frm.siblings('#form-head').find('h4').html("Something unexpected Happened. Please try again");
            frm.find('input[type=submit]').addClass('form-error');
            setTimeout(function(){
              frm.find('input[type=submit]').removeClass('form-error');
            }, 1000);
            
        }
    });
};

function delete_bulk() {
    console.log("in delete_bulk ajax fn");
    // var frm = $('#'+id);
    $.ajax({
        type: 'POST', //GET or POST as defined in HTML
        url: '/delete_bulk/', //action defined in HTML
        // data: frm.serialize(), //Serializing the object to pass through
        // handle a successful response
        success : function(json) {
            // frm[0].reset(); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            movies = json.count;
            frm.siblings('#form-head').find('h4').html(movies + " movies deleted!");
            exit_form();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            frm.find('input[type=submit]').val('Try Again').prop('disabled',true); //disable option
            frm.siblings('#form-head').find('h4').html("Something unexpected Happened. Please try again");
            frm.find('input[type=submit]').addClass('form-error');
            setTimeout(function(){
              frm.find('input[type=submit]').removeClass('form-error');
            }, 1000);
            
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
