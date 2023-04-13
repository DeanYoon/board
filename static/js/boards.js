$(document).ready(function() {
  $.ajax({
    type: "GET",
    url: "/api/boards",
    success: function(data) {
      for (var i = 0; i < data.length; i++) {
        var board = data[i];
        var listItem = $("<li></li>").appendTo($("#board-list"));
        var link = $("<a></a>").text(board.name).attr("href", "/boards/" + board.id + "/").appendTo(listItem);
      }
    }
  });
});
