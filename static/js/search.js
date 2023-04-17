$(document).ready(function() {
    $('form').submit(function(event) {
      event.preventDefault();
        var searchQuery = $('input[name="query"]').val();

        $.ajax({
            url: '/api/search',
            method: 'GET',
            data: {query: searchQuery},
            success: function(response) {
                // Handle the search results
                $('ul').empty();
                if (response.length == 0) {
                    $('ul').append('<h1>Posts not found</h1>');
                } else {
                  response.forEach(function(post) {
                    $('ul').append(`<li><a href="/boards/${post[6]}/posts/${post[0]}">${post[1]} -- ${post[7]}</a></li>`);
                  });
                }
            },
            error: function(xhr, status, error) {
                // Handle the error
                console.log(error);
            }
        });
      // TODO: send the search query to the server using AJAX
    });
  });
  

  $(document).on('click', '#back-to-board', function() {
    window.location.href = '/boards';
  });
  