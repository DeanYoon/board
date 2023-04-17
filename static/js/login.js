$(document).ready(function() {
    $('#login__form').on('submit', function(e) {
      e.preventDefault(); // prevent the form from submitting normally
      var formData = $(this).serialize(); // serialize the form data
  
      $.ajax({
        type: 'POST',
        url: '/api/login',
        data: formData,
          success: function (response) {
           
          alert(`Welcome ${response}!`); // show a success message
          window.location.href = '/boards'; // redirect to the boards page
        },
        error: function(xhr, status, error) {
          alert('Error: ' + xhr.responseText); // show an error message
          clearFormInputs()

        }
      });
    });
});
  


$(document).ready(function() {
    $('#sign-up__form').on('submit', function(e) {
      e.preventDefault(); // prevent the form from submitting normally
      var formData = $(this).serialize(); // serialize the form data
  
      $.ajax({
        type: 'POST',
        url: '/api/signup',
        data: formData,
        success: function(response) {
            alert(`Welcome ${response}!`); // show a success message
            window.location.href = '/boards'; // redirect to the boards page
        },
        error: function(xhr, status, error) {
          alert('Error: ' + xhr.responseText); // show an error message
          clearFormInputs()
        }
      });
    });
});




function clearFormInputs() {
    $('input[type="text"],input[type="password"]').each(function() {
        $(this).val('');
    });
}





