$(document).ready(function () {
  $("#login__form").on("submit", function (e) {
    e.preventDefault(); // prevent the form from submitting normally
    var formData = $(this).serialize(); // serialize the form data

    $.ajax({
      type: "POST",
      url: "/api/login",
      data: formData,
      success: function (response) {
        alert(`Welcome ${response}!`); // show a success message
        window.location.href = "/boards"; // redirect to the boards page
      },
      error: function (xhr, status, error) {
        alert("Error: " + xhr.responseText); // show an error message
        clearFormInputs();
      },
    });
  });
});

//password validation
$(document).ready(function () {
  $("#password2").keyup(function () {
    var password1 = $("#password1").val();
    var password2 = $("#password2").val();
    if (password1 != password2) {
      // Do something if passwords don't match
      $("#password-message").text("Passwords do not match");
    } else {
      // Do something if passwords match
      $("#password-message").text("");
    }
  });
});

$(document).ready(function () {
  $("#sign-up__form").on("submit", function (e) {
    e.preventDefault(); // prevent the form from submitting normally
    var formData = $(this).serialize(); // serialize the form data

    $.ajax({
      type: "POST",
      url: "/api/signup",
      data: formData,
      success: function (response) {
        alert(`Welcome ${response}!`); // show a success message
        window.location.href = "/boards"; // redirect to the boards page
      },
      error: function (xhr, status, error) {
        alert("Error: " + xhr.responseText); // show an error message
        clearFormInputs();
      },
    });
  });
});

function clearFormInputs() {
  $('input[type="text"],input[type="password"]').each(function () {
    $(this).val("");
  });
}
