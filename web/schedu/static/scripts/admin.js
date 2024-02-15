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
  performLogin('user1', 'password1');

  // Set up an interval to fetch and update data every 5 seconds
  setInterval(function () {
    // Fetch and update data only if the JWT token is available
    if (localStorage.getItem('jwtToken')) {
      fetchDataAndUpdate(localStorage.getItem('jwtToken'));
    }
  }, 5000); // 5000 milliseconds = 5 seconds

  // function to perform dashboard refresh on click
  $('.logo').on('click', function () {
    location.reload();
  }
  );

  // function to add dropdown functionality to REGISTRATION
  var $dropdown = $('.dropdown');
  var $dropdownContent = $('.dropdown-content');

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

  function openDropdown() {
      const dropdownHTML = `
          <li><a href="/register/student">Student</a></li>
          <li><a href="#">Teacher</a></li>
          <li><a href="/register/guardian">Guardian</a></li>`;

      $dropdownContent.html(dropdownHTML);
      $dropdown.addClass('open');
  }

  function closeDropdown() {
      $dropdownContent.empty();
      $dropdown.removeClass('open');
  }

// Function to show guardian section and hide student section
$('#guardianBtn').on('click', function () {
  $('#studentForm').hide();
  $('#guardianForm').show();
});

});
$('#studentForm').submit(function (e) {
  e.preventDefault(); // Prevent default form submission
  var formData = $(this).serialize(); // Serialize form data
  $.ajax({
    url: '/register/student', // Backend route for student registration
    type: 'POST',
    data: formData,
    success: function (response) {
      // Handle success response
      console.log('Student registration successful');
      // Optionally, redirect the user or show a success message
    },
    error: function (xhr, status, error) {
      // Handle error
      console.error('Error during student registration:', error);
      // Optionally, display an error message to the user
    }
  });
});

// Form submission handling for guardian registration
$('#guardianForm').submit(function (e) {
  e.preventDefault(); // Prevent default form submission
  var formData = $(this).serialize(); // Serialize form data
  $.ajax({
    url: '/register/guardian', // Backend route for guardian registration
    type: 'POST',
    data: formData,
    success: function (response) {
      // Handle success response
      console.log('Guardian registration successful');
      // Optionally, redirect the user or show a success message
    },
    error: function (xhr, status, error) {
      // Handle error
      console.error('Error during guardian registration:', error);
      // Optionally, display an error message to the user
    }
  });
});
