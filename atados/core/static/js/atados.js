( function ( w , $ , undefined ) {

  $('html').removeClass('no-js').addClass('js');

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $('.select-button-list li a').click(function(){
    li = $(this).parent('li');
    checkbox = $('[type=checkbox]', li);
    if (checkbox.is(':checked')) {
      checkbox.prop('checked', false);
      li.removeClass('active');
    } else {
      checkbox.prop('checked', true);
      li.addClass('active');
    }
    return false;
  });

  $('select[name="state"]').change(function(){
    var state = $(this)
    var city = state.closest('.location-fields').find('select[name="city"]');
    city.closest('.city-field').hide();
    if (state.val()) $.get('/city/' + state.val(), function(data) {
      city.find('option').remove()
      if (data.length > 1) {
        $.each(data, function() {
          city.append('<option value="' + this.id + '">' + this.name + '</option>')
        });
        city.closest('.city-field').show();
      }
    });
  });

  $('select[name="city"]').change(function(){
    var city = $(this)
    var suburb = city.closest('.location-fields').find('select[name="suburb"]');
    suburb.closest('.suburb-field').hide();
    if (city.val()) $.get('/suburb/' + city.val(), function(data) {
      suburb.find('option').remove()
      if (data.length > 1) {
        $.each(data, function() {
          suburb.append('<option value="' + this.id + '">' + this.name + '</option>')
        });
        suburb.closest('.suburb-field').show();
      }
    });
  });

}( window , window.jQuery ));
