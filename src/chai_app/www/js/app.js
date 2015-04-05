/* Page load functions */
// ========================= Register page functions ==========================
(function(){
  'use strict';

  // =============================== Login Page ===============================
  $(document).on('pageinit', '#login-page', function() {
    // Register button
    $('#register-button', this).on('click', function() {
      app.navi.pushPage('register.html');
    });
  });
  
  // =============================== Store page ===============================
  $(document).on('pageinit', '#store-page', function() {
    // Get options
    var options = app.navi.getCurrentPage().options;
    
    // Check for store_id
    // store_id is only passed if QR code for store is scanned
    if ("store_id" in options) {
      // Inside valid store
      
      // Send request for store menu
      var url = MAIN_URL + "c-menu/?store_id=" + options.store_id;
      $.getJSON(url, function(data) {
        // Store data as json string in hidden div
        $("#inventory-json").html(JSON.stringify(data));
        var html = ""; // empty inner HTML container to store new content
        var category; // string of category name from JSON response
        var content = document.getElementById("store-list");
        
        for (category in data) {
          // HTML for each category
          // Note: category may be lower case, so capitalize CSS is used
          if (!(jQuery.isEmptyObject(data[category]))) {
            // skip categories with no items
            html += "<ons-list-header " + 
                    "style=\"text-transform:capitalize;\">" +
                    category + "</ons-list-header>\n";
            var product;
            for (product in data[category]) {
              // Build HTML for each item
              // header
              var prod_id = data[category][product]['prod_id'];
              html += "<ons-list-item modifier=\"tappable\" id=\"prodid-" + 
                      prod_id + "\" class=\"list-item-container\" " + 
                      "onclick=\"select_options(this.id)\"><ons-row>";
              // product image
              html += "<ons-col width=\"105px\"><img src=\"" + 
                      IMG_URL + data[category][product]["img_url"] + 
                      "\" class=\"store-thumbnail\"></ons-col>\n" + 
                      "<ons-col>\n" + 
                      "<div class=\"store-name\">" + product + "</div>\n" + 
                      "<div class=\"store-feint\">Starting $" + 
                      parseFloat(
                        data[category][product]["price"]).toFixed(2) + 
                      "</div>\n" + "<div class=\"store-desc\">" + 
                      data[category][product]["prod_desc"] + "</div>\n" + 
                      "</ons-col>\n</ons-row>\n</ons-list-item>";
            };
          };
        };
        // Update store menu list
        content.innerHTML = html;
        ons.compile(content);
      });
    } else {
      // Not inside store, or not scanned QR yet
      ons.notification.alert({
        message: 'Please scan store QR code to continue.',
        title: 'Store Verification',
        buttonLabel: 'Scan Now',
        animation: 'default', // or 'none'
        // modifier: 'optional-modifier'
        callback: function() {
          scan();
        }
      });
    }
  });
  
})();        buttonLabel: 'Scan Now',
        animation: 'default', // or 'none'
        // modifier: 'optional-modifier'
        callback: function() {
          scan();
        }
      });
    }
  });
  
  // =============================== PayPal functions ================================
  //$(document).on('pageinit', '#paypal-page', function() {
    // Using paypal token, embed in-context express checkout page
    //var options = app.navi.getCurrentPage().options;
    //refresh_paypal_iframe(options.token);
    
  //});
  

})();