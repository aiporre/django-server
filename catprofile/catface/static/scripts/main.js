$(function(){
  // Submit post on submit
  // $('#post-form').on('submit', function(event){
  //   event.preventDefault();
  //   console.log("form submitted!")  // sanity check
  //   create_post();
  // });
  // AJAX functions
  // load_posts()
  load_cats()

  // Load 6 cats on the page
  function load_cats() {
      $.ajax({
          url : "api/v1/details/", // the endpoint
          type : "GET", // http method
          // handle a successful response
          success : function(json) {
              console.log('GET SUCESSFUL!');
              console.log(json[0])
              for (var i = 0; i < 6; i++) {
                  dateString = convert_to_readable_date(json[i].pub_date)
                  html_item = "<div class='col-lg-4 col-md-6 col-sm-12 text-center'>"+
                  "<img class='rounded-circle' alt='140x140' style='width: 140px; height: 140px;' src='"+
                  json[i].picturelink+"' data-holder-rendered='true'> <h3>" + json[i].cat.cat_name + "</h3> <p>" + json[i].description+"</p> </div>"
                  // console.log('HTML item: ', html_item)
                  $("#cats-top").prepend(html_item);
              }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });

  };
  // Load all posts on page load
  function load_posts() {
      $.ajax({
          url : "api/v1/details/", // the endpoint
          type : "GET", // http method
          // handle a successful response
          success : function(json) {
              console.log('GET SUCESSFUL!');
              console.log(json)
              for (var i = 0; i < json.length; i++) {
                  dateString = convert_to_readable_date(json[i].pub_date)
                  html_item = "<li id='cat-"+json[i].cat.id+"'><strong>"+json[i].cat.cat_name+
                      "</strong> - <span> "+dateString+
                      "</span> - <a id='delete-post-"+json[i].cat.id+"'> "+json[i].description+"</a></li>"
                  // console.log('HTML item: ', html_item)
                  $("#cats").prepend(html_item);
              }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });

  };
  // convert ugly date to human readable date
  function convert_to_readable_date(date_time_string) {
      var newDate = moment(date_time_string).format('MM/DD/YYYY, h:mm:ss a')
      return newDate
  }
})
