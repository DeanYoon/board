$(document).ready(function () {
  $("#add-board-button").click(function () {
    window.location.href = "/add_board/";
  });
  $("#logout-button").click(function () {
    window.location.href = "/";
  });
  $("#search-button").click(function () {
    window.location.href = "/search";
  });
  $("#add-board-form").on("submit", function (e) {
    e.preventDefault(); // prevent the form from submitting normally
    var formData = $(this).serialize(); // serialize the form data

    $.ajax({
      type: "POST",
      url: "/api/boards",
      data: formData,
      success: function (response) {
        window.location.href = "/boards";
      },
      error: function (xhr, status, error) {
        alert("Error: " + xhr.responseText);
      },
    });
  });
});
