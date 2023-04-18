$(document).ready(function () {
  $("form").submit(function (event) {
    event.preventDefault();
    var searchQuery = $('input[name="query"]').val();

    $.ajax({
      url: "/api/search",
      method: "GET",
      data: { query: searchQuery },
      success: function (response) {
        // Handle the search results
        $("ul").empty();
        if (response.length == 0) {
          $("ul").append("<h1>Posts not found</h1>");
        } else {
          response.forEach(function (post) {
            // create the span element
            var timeSpan = $("<span>")
              .attr("id", "time_left")
              .text(post.created_at);

            // create the anchor element
            var postAnchor = $("<a>")
              .attr("href", `/boards/${post.board_id}/posts/${post.id}`)
              .text(`${post.title} -- ${post.username}`);

            // add the span element to the anchor element
            postAnchor.append(timeSpan);

            // create the list item element and add the anchor element to it
            var listItem = $("<li>").append(postAnchor);

            // add the list item to the unordered list
            $("ul").append(listItem);
          });
        }
      },
      error: function (xhr, status, error) {
        // Handle the error
        console.log(error);
      },
    });
    // TODO: send the search query to the server using AJAX
  });
});

$(document).on("click", "#back-to-board", function () {
  window.location.href = "/boards";
});
