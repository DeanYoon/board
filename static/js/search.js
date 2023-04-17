$(document).ready(function() {
    $('form').submit(function(event) {
      event.preventDefault();
      var searchQuery = $('input[name="query"]').val();
        console.log(searchQuery);
        $.ajax({
            url: '/api/search',
            method: 'GET',
            data: {query: searchQuery},
            success: function(response) {
                // Handle the search results
                $.each(response, function(index, post) {
                    $('ul').append(`<li><a href="/boards/${post[6]}/posts/${post[0]}">${post[1]} -- ${post[7]}</a></li>`);

                });
            },
            error: function(xhr, status, error) {
                // Handle the error
                console.log(error);
            }
        });
      // TODO: send the search query to the server using AJAX
    });
  });
  