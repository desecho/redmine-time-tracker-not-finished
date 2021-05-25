function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie != '') {
    const cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function displayMessage(message) {
  return $.jGrowl(message);
};

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  crossDomain: false,  // obviate need for sameOrigin test
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type)) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$.jGrowl.defaults.closerTemplate = '<div>Close all notifications</div>';

$(function(){
  $(document).ajaxStart(function(){
    mprogress.start();
  });
  $(document).ajaxStop(function(){
    mprogress.end();
  });
});

var mprogress = new Mprogress();

var redmineTracker = function(){
    return {
      importProjects: function(){
        function error(){
          displayMessage('Error importing projects');
        }

        $.post(urlImportProjects, {}, function(response) {
          if (response.status == 'success') {
            window.location.reload();
          } else {
            error();
          }
        }).fail(function() {
          error();
        });
      },
      toggleProject: function(element, id){
        function error(){
          displayMessage('Error hiding/unhiding a project');
        }

        $.post(urlToggleProject, {'id': id}, function(response) {
          if (response.status == 'success') {
            var icon = $(element).find('i');
            icon.removeClass('fa-eye').removeClass('fa-eye-slash');
            if (response.is_hidden) {
              icon.addClass('fa-eye-slash');
            } else {
              icon.addClass('fa-eye');
            }
          } else {
            error();
          }
        }).fail(function() {
          error();
        });
      },
    }
}();
