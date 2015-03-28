/* Contains all page and helper functions for ready state */
ons.bootstrap();

// =================================== Globals ========================================
var main_url = "https://www.chaiapp.tk/" // Domain for backend
var img_url = main_url + "static/menu_img/" // URL for all menu images
var tax = 0.13; // Tax rate

// ============================= Login page functions =================================
function login() {
  loginInfo = {
    email : $('#email').val(),
    pass : $('#pass').val(),
  };
  alert("User: " + loginInfo.email + " Pass: " + loginInfo.pass);
  app.navi.pushPage('store.html');
};

// ============================ Register page functions ===============================
function register() {
  
  regInfo = {
    fname : $('#reg-fname').val(),
    lname : $('#reg-lname').val(),
    email : $('#reg-email').val(),
    pass : $('#pass-confirm1').val(),
    pass2: $('#pass-confirm2').val()
  };
  // Check password match
  if (regInfo.pass == regInfo.pass2) {
    // Format params for POST request
    if (regInfo.fname && 
        regInfo.lname && 
        regInfo.email && 
        regInfo.pass) {
      postParams = {
        fname : regInfo.fname,
        lname : regInfo.lname,
        email : regInfo.email,
        pass : regInfo.pass
      };
      
      // Send POST to register
      params = decodeURIComponent($.param(postParams, true));
      var url = main_url + "c-register/";
      xmlhttp = new XMLHttpRequest();
      xmlhttp.open("POST", url, true);
      xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
      xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4) {
          //alert(xmlhttp.status);
          //if (xmlhttp.status == 200 || xmlhttp.status == 0) {
        };
      };
      
      xmlhttp.send(params);
      //alert(xmlhttp.responseText);
      
      alert("Registered!");
      document.getElementById('email').value = postParams.email;
      app.navi.popPage();
    } else {
      alert("Please fill in all required fields.");
    };
  } else {
    alert("Passwords do not match! Please try again.");
  }; 
};

// =================================== Scan functions ===================================
function scan() {
  app.navi.resetToPage("store.html", {store_id: '12'}); // Used for testing purpose only
  /*
  window.plugins.barcodeScanner.scan( function(result) {
    
    if (result.text) {
      // Parse captured data
      captured = JSON.parse(result.text);
      
      // Scanned store QR code, redirect to store page of the captured store ID
      if ("store_id" in captured) {
        // Scanned QR contains store ID as an int string. (ie. "12")
        app.navi.resetToPage("store.html", {store_id: captured['store_id'],});
      };
      
    };
    
    
  }, function(error) {
    alert("Scanning error: " + error);
  });*/
};

// ============================ Option selection functions ==============================

// Select options for a menu item to add to cart
function select_options(prod_id) {
  // Retreive options data for the menu item selected
  // prod_id is an integer string required for the POST
  prod_id = prod_id.split("-")[1]; // Get product ID for POST params
  var url = main_url + "c-prod/?prod_id=" + prod_id; // POST URL for options JSON
  var html_str = ""; // container for building html string
  var product_obj = $("#prodid-" + prod_id); // referencing the menu DOM object pressed
  var prod_name = product_obj.find(".store-name").text();
  
  // Get POST response and build HTML string for options dialog
  
  var html_str = '<ons-list style="max-height:300px;">'; 
  
  $.getJSON(url, function(data) {
    // Response data format:
    // { op_id : { options_name : price difference }, ... }
    // ie. {"11": {"four cheese": "0"}, "10": {"plain": "0"}, "13": {"12 grain": "0"}, "12": {"sesame seed": "0"}}
    
    // Build HTML string within dialog
    var op_id;
    var op_count = 1; // Keep track of option, used for setting initial radio checked
    for (op_id in data) {
      var op_name;
      
      for (op_name in data[op_id]) {
        
        // Options pricing is determined by the base price + price difference
        var base_price = parseFloat(product_obj.find(".store-feint").text().split("$")[1]);
        
        // Check if it's a product with no options
        if (op_name == "") {
          // With empty option, this will also be the only option. 
          // Uses product name as option, and base price as price.
          
          // string format "Product ($###)":
          var op_text = title(product_obj.find(".store-name").text() + 
                        " ($" + base_price.toFixed(2).toString() + 
                        ")");
          
          // onclick captures html string selection, then changes a hidden div in the store page
          html_str += '<ons-list-item id="opid-' + 
                      op_id + 
                      '" class="op-list-item" ' + 
                      'onclick="option_select(this, \'' + op_id + '\')" ' + 
                      'modifier="tappable">' + 
                      '<label style="font-weight:normal" ' + 
                      'class="radio-button radio-button--list-item">';
          if (op_count == 1) {
             html_str += '<input type="radio" name="option" checked="checked">';
             option_replace(op_text, op_id); // Keep track of what's checked 
          } else {
             html_str += '<input type="radio" name="option">';
          };
          html_str += '<div class="radio-button__checkmark ' + 
                      'radio-button--list-item__checkmark"></div>' + 
                      op_text + '</label></ons-list-item>';

        } else {
          // If real options exist, use option name as the id tag and calculate new total price
          var new_price = parseFloat(data[op_id][op_name]) + base_price;
          var op_text = title(op_name + " ($" + new_price.toFixed(2).toString() + 
                        ")");
          
          html_str += '<ons-list-item id="opid-' + 
                      op_id + 
                      '" class="op-list-item" ' + 
                      'onclick="option_select(this, \'' + op_id + '\')" ' + 
                      'modifier="tappable">' + 
                      '<label style="font-weight:normal" ' + 
                      'class="radio-button radio-button--list-item">';
          if (op_count == 1) {
             html_str += '<input type="radio" name="option" checked="checked">';
             option_replace(op_text, op_id); // Keep track of what's checked in hidden div
          } else {
             html_str += '<input type="radio" name="option">';
          };
          html_str += '<div class="radio-button__checkmark ' + 
                      'radio-button--list-item__checkmark"></div>' + 
                      op_text + '</label></ons-list-item>';
          
        };
      };
      if (op_count == 1) {
        op_count = 2; // Only first count required for radio checklist default
      }
    };
    html_str += "</ons-list>";

    // Put HTML string into a dialog for option selection
    ons.notification.confirm({
      messageHTML: html_str,
      title: 'Select Option',
      buttonLabels: ['Cancel', 'Add to Cart'],
      animation: 'default',
      primaryButtonIndex: 1,
      cancelable: true,
      callback: function(index) {
        if (index==1) { // Add to Cart pressed
          selected = $("#options-content").html(); // format: "Large ($6.40) 123"
          // Add to cart
          cart_add(prod_name, selected);
        };
      }});
  });
};

function option_replace(html_str, op_id) {
  // Replace text within hidden div used to keep track of option selected
  // string format to save: "Large ($6.40) 123"
  $("#options-content").html(html_str + " " + op_id);
};

// New option selected changes hidden div value
function option_select(selection, op_id) {
  // string format to save: "Large ($6.40) 123"
  $("#options-content").html($(selection).text() + " " + op_id);
};

// =================================== Cart functions =====================================

// Show cart
function cart2() {
  ons.createDialog('cart_content.html').then(function(dialog) {
    dialog.show();
  });
};

function cart() {
  var cart_html = $("#cart-list").html();
  ons.notification.confirm({
    messageHTML: cart_html,
    title: 'Shopping Cart',
    buttonLabels: ['Keep Shopping', 'Checkout'],
    primaryButtonIndex: 1,
    animation: 'default',
    cancelable: true,
    callback: function(index) {
      // index: -1 cancel, 0 not yet, 1 checkout
      
    }
  });
}

// Add to cart
function cart_add(product, option) {
  // Adds product and option to cart.
  // Takes in string parameter for product and option (including price and ID)
  // Example: product = "Cafe Mocha" and option = "Large ($6.50) 123"
  // Saves html string to cart-content.html scrollable list
  
  // Build text string
  var op_name = $.trim(option.substring(0, option.indexOf("(")));
  var op_price = option.split("$")[1].split(")")[0];
  var op_id = option.split(") ")[1]; // format: "123"
  
  var cart_text;
  if (product == op_name) {
    // Option name can equal product if product has no options
    // format: "Product $price"
    var cart_text = op_name + " <b style='opacity:0.4;font-weight:normal;'>$" + 
                    op_price + "</b>";
  } else {
    // All other products with options
    // format: "Product (Option) $price"
    var cart_text = product + " <b style='opacity:0.4;font-weight:normal;'>(" + 
                    op_name + ") $" + op_price + "</b>";
  };
  
  // Check length to adjust line-height CSS property
  var line_height = "2.1";
  if (cart_text.length > 23) {
    line_height = "1";
  };
  
  // Build HTML string for cart update
  
  // format id tag for cart item: "cart-prodid-opid"
  var cart_id = "cart-" + get_prod_id(product) + "-" + op_id;
  var html_str = '<ons-list-item id="' + cart_id + '" class="cart-list-item">';
  // Cart text
  html_str += '<span style="line-height:' + line_height + 
              ';float:left; width:65%;vertical-align:middle;" class="cart-text">' + 
              cart_text + '</span><span style="float:right;vertical-align-middle;">';
  // Quantity buttons (default to 1 order when initially add to cart)
  html_str += '<a href="" style="vertical-align:middle;color:#f78f1f;" ' + 
              'class="fa fa-minus-circle fa-2x" onclick="cart_sub(this)"></a>&nbsp;&nbsp;&nbsp;' + 
              '<b class="cart-quantity" style="font-size:80%;vertical-align:middle;">1</b>&nbsp;&nbsp;&nbsp;' + 
              '<a href="" style="vertical-align:middle;color:#f78f1f;" ' + 
              'class="fa fa-plus-circle fa-2x" onclick="cart_plus(this)"></a>' + 
              '</span></ons-list-item>';
              
  
  // Update cart
  cart_append_html(html_str);
  
  // Disable item in store menu
  var prod_id = "prodid-" + get_prod_id(product);
  $("#" + prod_id).hide(); // hide menu item
  
  // Show cart
  cart();
};

// Append new order to cart (add to cart)
function cart_append_html(html_str) {
  // Internal function, used to append html string to cart 
  var current = $("#cart-list").html();
  $(html_str).insertBefore('#cart-total');
  cart_total_update();
};

// Cart update button (+)
function cart_plus(button_obj) {
  // Adds 1 to current object and cart variable
  quantity_obj = $(button_obj).parent().find(".cart-quantity") // dialog selector
  var quantity = parseInt(quantity_obj.text()) + 1;
  
  var cart_id = $(button_obj).parent().parent().attr('id');
  var cart_obj = $("#" + cart_id); // cart selector
  
  // Update dialog (does not affect actual value in cart)
  quantity_obj.text(quantity.toString()); 
  
  // Update actual value to cart
  cart_obj.find(".cart-quantity").text(quantity.toString());
  cart_total_update($(button_obj).parent().parent().parent());
};

// Cart update button (-)
function cart_sub(button_obj) {
  var quantity_obj = $(button_obj).parent().find(".cart-quantity") // dialog selector
  var quantity = parseInt(quantity_obj.text());
  
  var cart_id = $(button_obj).parent().parent().attr('id');
  var cart_obj = $("#" + cart_id); // cart selector
  
  if (quantity == 1) {
    
    // Show the hidden menu item since it's not in the cart anymore
    var text = cart_obj.text();
    if (text.indexOf("(") > -1) {
      // format: "Product (Option) $price"
      text = $.trim(text.split("(")[0]);
    } else {
      // format: "Product $price"
      text = $.trim(text.split("$")[0]);
    };
    $("#prodid-" + get_prod_id(text)).show();
    
    // Remove item from cart if only 1 left
    var root_cart = $(button_obj).parent().parent().parent();
    $(button_obj).parent().parent().remove(); // remove from dialog
    cart_obj.remove(); // remove from cart
    // Update cart
    cart_total_update(root_cart);
    
  } else if (quantity == 0) {
    // For future development to add quantity variable to option selection dialog.
    // Currently option selection dialog adds 1 quantity to cart each time.
    return;
    
  } else {
    // For all other values, subtract 1 from quantity
    quantity = quantity - 1;
    // Update dialog
    quantity_obj.text(quantity.toString());
    cart_obj.find(".cart-quantity").text(quantity.toString());
    cart_total_update($(button_obj).parent().parent().parent());
  };
}

// Recalculate and update cart total
function cart_total_update(object) {
  // Parameter is used only by cart window buttons
  var total = 0.00;
  
  //$("#cart-total-val").html("Total: $" + total.toFixed(2));
  if (arguments.length == 1) {
    // Used for updates made by cart window buttons. 
    // Loop through all cart items in the cart window
    $(object).find( ".cart-list-item" ).each(function( index ) {
      var quantity = parseInt($(this).find(".cart-quantity").text());
      var cart_text = $(this).find('.cart-text').text();
      var price = parseFloat(cart_text.substring(cart_text.indexOf("$")+1));
      total += (price * quantity);
    });
    $(object).find('#cart-total-val').html("Tax:&nbsp;&nbsp;&nbsp;$" + (tax * total).toFixed(2) + "<br/>" + 
                                           "Total:&nbsp;$" + (total+(total*tax)).toFixed(2));
  } else {
    // Used for all other global cart updates
    // Loop through all saved cart items in the store.html template
    $( ".cart-list-item" ).each(function( index ) {
      var quantity = parseInt($(this).find(".cart-quantity").text());
      var cart_text = $(this).find('.cart-text').text();
      var price = parseFloat(cart_text.substring(cart_text.indexOf("$")+1));
      total += (price * quantity);
    });
    $("#cart-total-val").html("Tax:&nbsp;&nbsp;&nbsp;$" + (tax * total).toFixed(2) + "<br/>" + 
                              "Total:&nbsp;$" + (total+(total*tax)).toFixed(2));
  }
}

// ================================= Other helper functions =================================

// title case helper function
function title(str) {
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

// Get product ID based on product name
function get_prod_id(prod_name) {
  var store_menu = JSON.parse($("#inventory-json").text());
  // Find html id tag for product in store menu using the json menu
  var cat;
  for (cat in store_menu) {
    var prod;
    for (prod in store_menu[cat]) {
      if (prod == prod_name) {
        return store_menu[cat][prod]['prod_id'];
      };
    };
  };
};














