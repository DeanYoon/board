$(document).ready(function () {
  $("#add-board-button").click(function () {
    window.location.href = "/add_board/";
  });
});
$(document).ready(function () {
  $("#logout-button").click(function () {
    window.location.href = "/";
  });
});

$(document).ready(function () {
  $("#search-button").click(function () {
    window.location.href = "/search";
  });
});

$(document).ready(function () {
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
