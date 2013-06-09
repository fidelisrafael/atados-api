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

  $('[name="can_be_done_remotely"]').change(function(){
    var container = $(this).parents('fieldset').find('.location-fields');
    if ($(this).is(':checked')) {
      container.hide();
      container.addClass('hide');
    } else {
      container.show();
      container.removeClass('hide');
    }
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

    $('.role-forms', roles).append(clone);
  });

  $('.infinite-navigation .more').click(function() {
    $('.project-list.infinite').infinitescroll('resume');
    $('.project-list.infinite').scroll();
    $('.infinite-navigation').hide();
    return false;
  });

  $('.project-list-filter .update').click(function() {
    $('.project-list.infinite').addClass('empty');
    $('.project-list.infinite').empty();

    if ($(w).scrollTop() > $('#list').offset().top) {
      $('html, body').scrollTop($('#list').offset().top);
    }

    $('.project-list.infinite').infinitescroll({
      state: {
        currPage: 0,
      },
      path: function(page) {
        if ($('#filter-project').is(":visible")) {
          var path = '/api/v1/project';
          var forms = $('#filter-project :input[value][value!=""]');
        } else {
          var path = '/api/v1/nonprofit';
          var forms = $('#filter-nonprofit :input[value][value!=""]');
        }

        path += '?page=' + page;

        forms.each(function() {
          var query = $(this).serialize();
          if (query) path += '&' + query;
        });

        return path;
      }
    });
    $('.project-list.infinite').infinitescroll('resume');
    $('.project-list.infinite').scroll();
    $('.infinite-navigation').hide();
    return true;
  });

  $('.project-list.infinite').infinitescroll({
    loading: {
      msg: $('<span>...</span>'),
      selector: '.infinite-preloader',
    },
    path: function(page) {
      return '/api/v1/project?page=' + page;
    },
    dataType: 'json',
    appendCallback: false,
  }, function(json, opts) {
    if (json.length === 0) {
      $('.project-list.infinite').infinitescroll('pause');
      $('.project-list.infinite').removeClass('empty');
      return false;
    }

    if (opts.state.currPage == 3) {
      $('.project-list.infinite').infinitescroll('pause');
      $('.infinite-navigation').show();
    }

    container = $(this);
    var row;
      
    for (var key in json) {
      project = json[key];
      if (key % 3 == 0) {
        if (key > 0)
          row.hide().appendTo(container).fadeIn();
        row = $('<div class="row"></div>');
      }

      var item = $(
        '<div class="span3 project-item">' + 
          '<a href="' + project.url + '">' + 
            '<img alt="' + project.name + '"  src="' + project.image + '" width="270" height="180">' +
          '</a>' +
          '<a class="well-title" href="' + project.url + '">' + project.name + '</a>' +
          '<p class="description">' + project.details + '</p>' +
        '</div>');

      if (project.nonprofit) {
        item.append(
          '<div class="nonprofit">' +
            '<a href="' + project.nonprofit.url + '" class="picture">' + 
              '<img alt="' + project.nonprofit.name + '" src="' + project.nonprofit.image + '" width="34" height="34">' +
            '</a>' +
            '<a href="' + project.nonprofit.url + '" class="name">' + project.nonprofit.name + '</a>' +
            '<div class="volunteers"><i class="icon icon-volunteer"></i> <span>' + project.volunteers + '</span></div>' +
          '</div>');
      }

      row.append(item);
    }

    row.hide().appendTo(container).fadeIn();

    $('.project-list.infinite').removeClass('empty');
  });

}( window , window.jQuery ));
