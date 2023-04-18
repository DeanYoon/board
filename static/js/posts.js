$(document).ready(function () {
  $("#add-post-button").click(function () {
    window.location.href = "add_post";
  });

  $("#back-board-button").click(function () {
    window.location.href = "/boards";
  });

  //post 추가 api호출
  $("#add-post-form").submit(function (event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    var board_id = window.location.href.split("/")[4];

    // Serialize the form data
    var formData = $(this).serialize();
    console.log(formData);
    // Send an AJAX request to the add post API
    $.ajax({
      type: "POST",
      url: `/api/boards/${board_id}/posts`,
      data: formData,
      success: function (response) {
        // Redirect to the posts page for the current board
        window.location.href = `/boards/${board_id}/`;
      },
      error: function (xhr, status, error) {
        // Show an error message
        alert("Error: " + xhr.responseText);
      },
    });
  });

  //포스트 수정 페이지로 이동
  $("#edit-post-button").click(function () {
    var url = window.location.href;
    var segments = url.split("/");
    const board_id = segments[4];
    const post_id = segments[6];
    window.location.href = `/boards/${board_id}/posts/${post_id}/edit`;
  });

  //paging 처리 in posts
  $("#page-links a").click(function (event) {
    event.preventDefault();
    const page = $(this).data("page");
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set("page", page);
    window.location.href = currentUrl.href;
  });

  //params 에 따른 페이지 select 값 고정 및 값 변화시 per_page변경
  // Get the per page value from the query parameter
  const urlParams = new URLSearchParams(window.location.search);
  const perPage = urlParams.get("per_page") || 10;
  const currentPage = parseInt(urlParams.get("page")) || 1;
  // Loop through all the page links and add the "active" class to the current page link
  $("#page-links a").each(function () {
    if ($(this).data("page") == currentPage) {
      $(this).addClass("active");
    } else {
      $(this).removeClass("active");
    }
  });

  $(document).ready(function () {});

  // list number change depending page and per_page value
  var startNum = perPage * (currentPage - 1) + 1;
  $("#posts-ol").attr("start", startNum);

  // Set the selected option based on the per page value
  $("#per-page").val(perPage);
  $("#per-page").change(function () {
    var perPage = $(this).val();
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set("per_page", perPage);
    currentUrl.searchParams.set("page", 1);
    window.location.href = currentUrl.href;
    $("#per-page").val(perPage);
  });

  //포스트 삭제 api 실행
  $("#delete-post-button").click(function () {
    var url = window.location.href;
    var segments = url.split("/");
    const board_id = segments[4];
    const post_id = segments[6];
    if (confirm("Are you sure you want to delete this post?")) {
      $.ajax({
        url: `/api/boards/${board_id}/posts/${post_id}`,
        type: "DELETE",
        success: function (result) {
          console.log(result);
          window.location.href = `/boards/${board_id}/`;
        },
        error: function (xhr, status, error) {
          console.log(error);
        },
      });
    }
  });

  //포스팅 목록으로 돌아가는 함수
  $("#back-post-button").click(function () {
    var url = window.location.href;
    var segments = url.split("/");
    const board_id = segments[4];

    window.location.href = `/boards/${board_id}/`;
  });

  //포스팅 수정 api 호출
  $("#edit-post-form").submit(function (event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    var url = window.location.href;
    var urlParts = url.split("/");
    var board_id = urlParts[4];
    var post_id = urlParts[6];

    // Get the form data
    var formData = $(this).serialize();

    // Send an AJAX request to the edit post API
    $.ajax({
      type: "POST",
      url: `/api/boards/${board_id}/posts/${post_id}`,
      data: formData,
      success: function (response) {
        // Show a success message
        alert("Post edited successfully!");
        window.location.href = `/boards/${board_id}/posts/${post_id}`;
      },
      error: function (xhr, status, error) {
        // Show an error message
        alert("Error: " + xhr.responseText);
      },
    });
  });
});

function getUrlParam(param, defaultValue) {
  const params = new URLSearchParams(window.location.search);
  return params.get(param) || defaultValue;
}
