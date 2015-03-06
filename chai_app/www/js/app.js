(function(){
  'use strict';

  var currentItem = {};
  var url = "http://www.chaiapp.tk/"

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
      url += "c-menu/?store_id=" + options.store_id;
      $.getJSON(url, function(data) {
        alert("query success: shop " + options.store_id);
        //alert(JSON.stringify(data));
        var html = "";
        var category;
        for (category in data) {
          html += "ASDF";
          //alert(category);
          //alert(JSON.stringify(data[x]));
          
        }
      });
    } else {
      // Not inside store, or not scanned QR yet
      //alert(JSON.stringify(options));
    }
  });
  
  

})();