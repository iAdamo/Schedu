/* global location */
$(document).ready(function () {
  // Set up an interval to fetch and update data every 5 seconds
  setInterval(fetchDataAndUpdate, 5000); // 5000 milliseconds = 5 seconds

  // Refresh dashboard on logo click
  $('.logo').on('click', location.reload);

  // Add dropdown functionality to REGISTRATION
  setupDropdown();

  // Show guardian section and hide student section on next button click
  $('#nextbutton').on('click', showGuardianForm);

  // Search functionality
  setupSearch();

  // Load user profile
  loadUserProfile();
});

// function performLogin(username, password) {
//  $.ajax({
//    url: 'http://127.0.0.1:5001/api/v1/login',
//    type: 'POST',
//    contentType: 'application/json',
//    data: JSON.stringify({ username, password }),
//    success: function (data) {
//      localStorage.setItem('jwtToken', data.access_token);
//      fetchDataAndUpdate();
//    },
//    error: function (xhr, status, error) {
//      console.error('Error during login:', error);
//    }
//  });
// }

function fetchDataAndUpdate () {
  $.ajax({
    url: 'http://127.0.0.1:5001/api/v1/stats',
    type: 'GET',
    contentType: 'application/json',
    success: function (data) {
      $('.card h1.student').text(data.Student);
      $('.card h1.teacher').text(data.Teacher);
      $('.card h1.guardian').text(data.Guardian);
      $('.card h1.admin').text(data.Admin);
    },
    error: function (xhr, status, error) {
      console.error('Error fetching data:', error);
    }
  });
}

function setupDropdown () {
  const $dropdown = $('.dropdown');
  const $dropdownContent = $('.dropdown-content');

  $dropdown.on('click', function (e) {
    e.stopPropagation();
    $dropdown.hasClass('open') ? closeDropdown() : openDropdown();
  });

  $(document).on('click', function (e) {
    if (!$(e.target).closest('.dropdown').length) {
      closeDropdown();
    }
  });

  function openDropdown () {
    const dropdownHTML = `
      <li><a href="/register/student">Student</a></li>
      <li><a href="/register/teacher">Teacher</a></li>
      <li><a href="/register/guardian">Guardian</a></li>`;
    $dropdownContent.html(dropdownHTML);
    $dropdown.addClass('open');
  }

  function closeDropdown () {
    $dropdownContent.empty();
    $dropdown.removeClass('open');
  }
}

function showGuardianForm () {
  $('#studentForm').hide();
  $('#guardianForm').show();
}

function setupSearch () {
  $('#searchInput').on('input', function () {
    const Name = $(this).val();
    if (!Name.trim()) {
      $('#searchResults').empty();
      return;
    }
    searchByName(Name);
  });

  $(document).on('click', function (event) {
    if (!$(event.target).closest('#searchInput, #searchResults').length) {
      $('#searchResults').empty();
    }
  });

  $('#searchInput').on('input', function () {
    $(this).val() ? $('#cancelButton').show() : $('#cancelButton').hide();
  });

  $('#cancelButton').on('click', function () {
    $('#searchInput').val('');
    $('#searchResults').empty();
    $(this).hide();
  });
}

function searchByName (Name) {
  $.ajax({
    url: 'http://127.0.0.1:5001/api/v1/search/' + Name,
    type: 'GET',
    contentType: 'application/json',
    success: displayResults,
    error: function (error) {
      console.error('Error in search:', error);
    }
  });
}

function displayResults (data) {
  const resultsDiv = $('#searchResults');
  resultsDiv.empty();

  if (!data || data.length === 0) {
    resultsDiv.append('<p>No results found.</p>');
    return;
  }

  data.forEach(function (item) {
    const result = `<li><a href="/profile/${item.id}"> ${item.name} </a></li>`;
    resultsDiv.append(result);
  });
}

function loadUserProfile () {
  const profilePathRegex = /^\/profile\/[-a-zA-Z0-9]+$/;
  if (!profilePathRegex.test(window.location.pathname)) return;

  const userId = window.location.pathname.split('/').pop();
  $.ajax({
    url: 'http://127.0.0.1:5001/api/v1/profile/' + userId,
    type: 'GET',
    contentType: 'application/json',
    success: function (data) {
      for (const key in data) {
        if (key !== 'password' && key !== '__class__') {
          $('#' + key).text(data[key]);
        }
      }
    }
  });
}
