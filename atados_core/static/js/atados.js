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
    var suburb = city.closest('.location-fields').find('select[name="suburb"]');
    city.closest('.city-field').hide().find('option').remove();
    suburb.closest('.suburb-field').hide().find('option').remove();
    if (state.val()) $.get('/city/' + state.val(), function(data) {
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
    suburb.closest('.suburb-field').hide().find('option').remove();
    if (city.val()) $.get('/suburb/' + city.val(), function(data) {
      if (data.length > 1) {
        $.each(data, function() {
          suburb.append('<option value="' + this.id + '">' + this.name + '</option>')
        });
        suburb.closest('.suburb-field').show();
      }
    });
  });

  $('.roles .add').click(function() {
    var roles = $(this).closest('.roles');
    var clone = $('.empty-form', roles).clone().removeClass('empty-form').removeClass('hide');
    var total_forms = parseInt($('[name="form-TOTAL_FORMS"]', roles).val());
    var max_num_forms = parseInt($('[name="form-MAX_NUM_FORMS"]', roles).val());

    if (total_forms++ > max_num_forms) return;

    $('[name="form-TOTAL_FORMS"]', roles).val(total_forms);
    
    $('input, textarea', clone).each(function(index, element) {
      $(element).attr('id', $(element).attr('id').replace('__prefix__', String(total_forms - 1)));
      $(element).attr('name', $(element).attr('name').replace('__prefix__', String(total_forms - 1)));
    });

    clone.insertBefore($(this));
  });

}( window , window.jQuery ));
