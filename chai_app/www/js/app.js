(function(){
  'use strict';

  var currentItem = {};
  var main_url = "http://www.chaiapp.tk/"
  var img_url = main_url + "static/menu_img/"

  $(document).on('pageinit', '#detail-page', function() {
    $('.item-title', this).text(currentItem.title);
    $('.item-desc', this).text(currentItem.desc);
    $('.item-label', this).text(currentItem.label);
    $('.add-note-action-item', this).click(function () {
        alert('dummy message');
    });
  });

  $(document).on('pageinit', '#list-page', function() {
    $('.item', this).on('click', function() {
      currentItem = {
        title : $('.item-title', this).text(),
        desc : $('.item-desc', this).text(),
        label : $('.item-label', this).text()
      };

      app.navi.pushPage('detail.html');
    });
  });
  
  // Login Page
  $(document).on('pageinit', '#login-page', function() {
    // Register button
    $('#register-button', this).on('click', function() {
      app.navi.pushPage('register.html');
    });
  });
  /* Login page functions */
  
  // Store page
  $(document).on('pageinit', '#store-page', function() {
    // Get options
    
    var options = app.navi.getCurrentPage().options;
    
    // Check for store_id
    // store_id is only passed if QR code for store is scanned
    if ("store_id" in options) {
      // Inside valid store
      //alert("store_id: " + options.store_id);
      var url = main_url + "c-menu/?store_id=" + options.store_id;
      $.getJSON(url, function(data) {
        //alert("query success: shop " + options.store_id);
        // alert(JSON.stringify(data));
        var html = ""; // empty inner HTML container to store new content
        var category; // string of category name from JSON response
        var content = document.getElementById("store-list"); // HTML element of the store page menu list
        
        for (category in data) {
          // HTML for each category
          // Note: category may be lower case, so capitalize CSS is used
          html += "<ons-list-header style=\"text-transform:capitalize;\">" + category + "</ons-list-header>\n";
          var product;
          for (product in data[category]) {
            // HTML for each item
            // header
            html += "<ons-list-item modifier=\"tappable\" class=\"list-item-container\"><ons-row>";
            // product image
            html += "<ons-col width=\"105px\"><img src=\"" + img_url + data[category][product]["img_url"] + "\" class=\"store-thumbnail\"></ons-col>\n";
            //html += "<ons-col width=\"165px\"><img src=" + "http://www.chaiapp.tk/static/menu_img/breakf-hash-brown.png" + "\" class=\"store-thumbnail\"></ons-col>\n";
            // product info
            html += "<ons-col>\n";
            html += "<div class=\"store-name\">" + product + "</div>\n";
            html += "<div class=\"store-feint\">Starting $" + parseFloat(data[category][product]["price"]).toFixed(2) + "</div>\n";
            html += "<div class=\"store-desc\">" + data[category][product]["prod_desc"] + "</div>\n";
            html += "</ons-col>\n</ons-row>\n</ons-list-item>";
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
      //alert(JSON.stringify(options));
      var content = document.getElementById("store-list"); // HTML element of the store page menu list
      content.innerHTML = "Please verify your presence by scanning the store QR code.";
    }
  });
  
  

})();