/* Page load functions */

(function(){
  'use strict';

  // =================================== Login Page ===================================
  $(document).on('pageinit', '#login-page', function() {
    // Register button
    $('#register-button', this).on('click', function() {
      app.navi.pushPage('register.html');
    });
  });
  
  // =================================== Store page ===================================
  $(document).on('pageinit', '#store-page', function() {
    // Get options
    
    var options = app.navi.getCurrentPage().options;
    
    // Check for store_id
    // store_id is only passed if QR code for store is scanned
    if ("store_id" in options) {
      // Inside valid store
      // Send request for store menu
      var url = main_url + "c-menu/?store_id=" + options.store_id;
      $.getJSON(url, function(data) {
        // Store data as json string in hidden div
        $("#inventory-json").html(JSON.stringify(data));
        var html = ""; // empty inner HTML container to store new content
        var category; // string of category name from JSON response
        var content = document.getElementById("store-list"); // HTML element of the store page menu list
        
        for (category in data) {
          // HTML for each category
          // Note: category may be lower case, so capitalize CSS is used
          html += "<ons-list-header style=\"text-transform:capitalize;\">" + 
                  category + "</ons-list-header>\n";
          var product;
          for (product in data[category]) {
            // HTML for each item
            // header
            var prod_id = data[category][product]['prod_id']; // required for options selection
            html += "<ons-list-item modifier=\"tappable\" id=\"prodid-" + 
                    prod_id + "\" class=\"list-item-container\" " + 
                    "onclick=\"select_options(this.id)\"><ons-row>";
            // product image
            html += "<ons-col width=\"105px\"><img src=\"" + 
                    img_url + data[category][product]["img_url"] + 
                    "\" class=\"store-thumbnail\"></ons-col>\n" + 
                    "<ons-col>\n" + 
                    "<div class=\"store-name\">" + product + "</div>\n" + 
                    "<div class=\"store-feint\">Starting $" + 
                    parseFloat(data[category][product]["price"]).toFixed(2) + 
                    "</div>\n" + "<div class=\"store-desc\">" + 
                    data[category][product]["prod_desc"] + "</div>\n" + 
                    "</ons-col>\n</ons-row>\n</ons-list-item>";
          }
          //alert(JSON.stringify(data[x]));
        }
        // Update store menu list
        //content.innerHTML="<ons-list-header style=\"text-transform:capitalize;\">coffee</ons-list-header>";
        //content.innerHTML += "<ons-list-item modifier=\"tappable\">asdf</ons-list-item>"
        content.innerHTML = html;
        ons.compile(content);
      });
    } else {
      // Not inside store, or not scanned QR yet
      ons.notification.alert({
        message: 'Please scan store QR code to continue.',
        title: 'Store Verification',
        buttonLabel: 'Scan Now (Skipped for testing)',
        animation: 'default', // or 'none'
        // modifier: 'optional-modifier'
        callback: function() {
          scan();
        }
      });
    }
  });
  
  

})();        content.innerHTML = html;
        ons.compile(content);
      });
    } else {
      // Not inside store, or not scanned QR yet
      //alert(JSON.stringify(options));
      var content = document.getElementById("store-list"); // HTML element of the store page menu list
      content.innerHTML = "Please verify your presence by scanning the store QR code.";
    }
  });
  
  

})();