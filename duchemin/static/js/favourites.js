var attachFavouritesAction = function() {
    $('.favourites-link').on({
        'click': function(event) {
            event.preventDefault();
            $.ajax({
                url: $(this).attr('href'),
                context: this,
                success: function(data) {
                    if (data['action'] == 'remove') {
                        $(this).empty();
                        $(this).attr('href', "/favourite/" + data['content'] + "?add");
                        $(this).append('<i class="icon-star"></i> Add to Favorites');
                    } else {
                        $(this).empty();
                        $(this).attr('href', "/favourite/" + data['content'] + "?remove");
                        $(this).append('<i class="icon-star-empty"></i> Remove from Favourites');
                    }
                }
            });
        }
    });
};