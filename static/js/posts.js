$(document).ready(function () {
  $("#add-post-button").click(function () {
    window.location.href = "add_post";
  });
});

$(document).ready(function () {
  $("#back-board-button").click(function () {
    window.location.href = "/boards";
  });
});

//post 추가 api호출
$(document).ready(function () {
  $("#add-post-form").submit(function (event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    var board_id = window.location.href.split("/")[4];

    // Serialize the form data
    var formData = $(this).serialize();
    console.log(formData)
    // Send an AJAX request to the add post API
    $.ajax({
      type: 'POST',
      url: `/api/boards/${board_id}/posts`,
      data: formData,
      success: function (response) {
        // Redirect to the posts page for the current board
        window.location.href = `/boards/${board_id}/`;
      },
      error: function (xhr, status, error) {
        // Show an error message
        alert('Error: ' + xhr.responseText);
      }
    });
  });
});
//포스트 수정 페이지로 이동
$(document).ready(function () {
  $("#edit-post-button").click(function () {
    var url = window.location.href;
    var segments = url.split("/");
    const board_id = segments[4];
    const post_id = segments[6];
    window.location.href = `/boards/${board_id}/posts/${post_id}/edit`;
  });
});

//포스트 삭제 api 실행
$(document).ready(function () {
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
          $('<button id="save-edit-comment-button">')
            .data("comment-id", commentId)
            .text("Save")
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

//포스팅 목록으로 돌아가는 함수
$(document).ready(function () {
  $("#back-post-button").click(function () {
    var url = window.location.href;
    var segments = url.split("/");
    const board_id = segments[4];

    window.location.href = `/boards/${board_id}/`;
  });
});


//좋아요 버튼 클릭시 api 호출
$(document).on('click', '.like-comment-button', function() {
  var commentId = $(this).data('comment-id');
  console.log(commentId)
  $.ajax({
    url: '/api/comments/' + commentId + '/like',
    type: 'POST',
    success: function(response) {
      location.reload();
      // Add code here to update the UI to show that the comment has been liked
    },
    error: function(error) {
      console.log('Error liking comment:', error);
    }
  });
});


