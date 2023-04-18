$(document).ready(function () {
  $("#comment-form").submit(function (event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get the board and post IDs from the URL
    var board_id = window.location.href.split("/")[4];
    var post_id = window.location.href.split("/")[6];

    // Serialize the form data
    var formData = $(this).serialize();
    // Send an AJAX request to the server
    $.ajax({
      type: "POST",
      url: `/api/boards/${board_id}/posts/${post_id}/comments`,
      data: formData,
      success: function (response) {
        // Handle the successful response
        // TODO: Update the page with the new comment

        location.reload();
      },
      error: function (xhr, status, error) {
        // Handle the error response
        window.location.href = `/`;
      },
    });
  });
});

//좋아요 버튼 클릭시 api 호출
$(document).on("click", ".like-comment-button", function () {
  var commentId = $(this).data("comment-id");
  $.ajax({
    url: "/api/comments/" + commentId + "/like",
    type: "POST",
    success: function (response) {
      location.reload();
      // Add code here to update the UI to show that the comment has been liked
    },
    error: function (error) {
      console.log("Error liking comment:", error);
      window.location.href = `/`;
    },
  });
});

//댓글수정 버튼 클릭시 텍스트가 input 으로 변하게

$(document).ready(function () {
  $(".edit-comment-button").click(function () {
    var commentId = $(this).data("comment-id");
    var commentText = $(this).parent().find(".comment_text").text();
    $(this)
      .parent()
      .empty()
      .append(
        $("<form>").append(
          $('<input type="text" class="edit-comment-text">').val(commentText),
          $('<input type="submit" id="save-edit-comment-button">').data(
            "comment-id",
            commentId
          )
        )
      );
    setTimeout(function () {
      $(".edit-comment-text").focus();
    }, 0);
  });
  // Click event handler for the save edit comment button
  $(document).on("click", "#save-edit-comment-button", async function () {
    var commentId = $(this).data("comment-id");
    var editedCommentText = $(this).prev(".edit-comment-text").val();

    await $.ajax({
      url: "/api/comments/" + commentId,
      type: "PUT",
      data: {
        comment_text: editedCommentText,
      },
      success: function (response) {
        location.reload();
      },
      error: function (error) {
        console.log(error);
      },
    });
    // Add code here to save the edited comment
  });
});

//댓글 삭제 api 실행
$(document).ready(function () {
  $(".delete-comment-button").click(function () {
    var commentId = $(this).data("comment-id");
    $.ajax({
      url: "/api/comments/" + commentId,
      type: "DELETE",
      success: function (result) {
        location.reload();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log(errorThrown);
      },
    });
  });
});
