$(document).ready(function () {
  // Function to perform login and get a JWT token
  function performLogin (username, password) {
    $.ajax({
      url: 'http://127.0.0.1:5001/api/v1/login',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ username, password }),
      success: function (data) {
        // Store the JWT token securely (e.g., in localStorage or a secure cookie)
        localStorage.setItem('jwtToken', data.access_token);

        // Fetch and update data using the JWT token
        fetchDataAndUpdate(data.access_token);
      },
      error: function (xhr, status, error) {
        console.error('Error during login:', error);
      }
    });
  }

  // Function to fetch and update the data using a JWT token
  function fetchDataAndUpdate (jwtToken) {
    $.ajax({
      url: 'http://127.0.0.1:5001/api/v1/stats',
      type: 'GET',
      contentType: 'application/json',
      headers: {
        Authorization: 'Bearer ' + jwtToken
      },
      success: function (data) {
        // Update the content of HTML elements with the fetched data
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

  // Example usage
  performLogin('admin', 'admin');

  // Set up an interval to fetch and update data every 5 seconds
  setInterval(function () {
    // Fetch and update data only if the JWT token is available
    if (localStorage.getItem('jwtToken')) {
      fetchDataAndUpdate(localStorage.getItem('jwtToken'));
    }
  }, 50000); // 5000 milliseconds = 5 seconds

  // function to perform dashboard refresh on click
  $('.logo').on('click', function () {
    location.reload();
  }
  );

  // function to add dropdown functionality to REGISTRATION
  const $dropdown = $('.dropdown');
  const $dropdownContent = $('.dropdown-content');

  $dropdown.on('click', function (e) {
    e.stopPropagation();

    if ($dropdown.hasClass('open')) {
      closeDropdown();
    } else {
      openDropdown();
    }
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

  // Function to show guardian section and hide student section
  $('#nextbutton').on('click', function () {
    $('#studentForm').hide();
    $('#guardianForm').show();
  });

  // Search functionality
  $('#searchInput').on('input', function () {
    const Name = $(this).val();

    // Check if the search term is empty and clear the results if needed
    if (!Name.trim()) {
      $('#searchResults').empty();
      return;
    }
    searchByName(Name, localStorage.getItem('jwtToken'));
  });
  // Function to perform search by name
  function searchByName (Name, jwtToken) {
    $.ajax({
      url: 'http://127.0.0.1:5001/api/v1/search',
      type: 'POST',
      contentType: 'application/json',
      headers: {
        Authorization: 'Bearer ' + jwtToken
      },
      data: JSON.stringify({ name: Name }),
      success: function (data) {
        displayResults(data);
      },
      error: function (error) {
        console.error('Error in search:', error);
      }
    });
  }
  // Function to display search results
  function displayResults (data) {
    const resultsDiv = $('#searchResults');
    resultsDiv.empty();

    if (!data || data.length === 0) {
      resultsDiv.append('<p>No results found.</p>');
    } else {
      data.forEach(function (result) {
        resultsDiv.append('<li><a href="/profile">' + result + '</a></li>');
      });
    }
  }
  // Function to close search results when clicking outside the search input
  $(document).on('click', function (event) {
    if (!$(event.target).closest('#searchInput, #searchResults').length) {
      $('#searchResults').empty();
    }
  });
  // Function to clear search input and hide cancel button
  $('#searchInput').on('input', function () {
    if ($(this).val()) {
      $('#cancelButton').show();
    } else {
      $('#cancelButton').hide();
    }
  });
  // Function to clear search input and hide cancel button
  $('#cancelButton').on('click', function () {
    $('#searchInput').val('');
    $('#searchResults').empty();
    $(this).hide();
  });
});
