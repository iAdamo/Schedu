$(document).ready(function () {
  // Function for the transition effect
  setTimeout(function () {
    $('#transition-container').css('opacity', 0);
    $('#content').css('opacity', 1).show();

    setTimeout(function () {
      if (window.location.pathname === '/') {
        window.location.href = '/auth/sign_in';
      }
    }, 500);
  }, 5000);
});
