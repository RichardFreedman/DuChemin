function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

var MILLISECONDS_IN_DAY = 86400000

// Helper function to start appropriate timeout loop for comments feed
function startCommentFeed(piece, days_to_show){

    // First fetch has id 0, so it gets everything
    var last_update = 0;
    var timeout = 2000;
    
    // Check to see if the helper function was called with a piece_id or not
    if (piece != null){
        updatePieceComments(piece, days_to_show);
    } else {
        updateAllComments(days_to_show);
    }

    // Logic to handle getting and displaying all comments
    function updateAllComments(days_to_show) {
        $.ajax({
            type: "GET",
            url: "/comments/",
            cache: false,
            data: {
                'last_update': last_update,
                },             
            dataType: 'json',
            success: function (json) {
                $.each(json.results, function(i,item) {
                    // Isn't there any way to get the full name, such as
                    // `item.author.first_name + item.author.last_name` ?
                    // I thought item.author was of the User model.

                    // Also, I surrounded the comments in a <p> element,
                    // which should be fine. Without it, the margins are
                    // terrible. Another way to do it might be to modify
                    // the CSS to add margin to .comment blocks.

                    // Todo: serialize userprofile so we can link to person page

                    var comment = '<div class="comment"><div class="author">' +
                        "<h5><a href='/piece/" + item.piece.piece_id + "'>" +
                        item.piece.piece_id + '</a> &bull; ' +
                        item.author.first_name + ' ' + item.author.last_name +
                        '</a> &bull; ' + item.created.replace(/T.+$/gi,"") +
                        '</h5></div>' +
                        '<div class="text"><p>' + parseCommentTags(item.text) +
                        '</p></div></div>';

                    // Check the date of the comment against the current date,
                    //   and only prepend if it's a recent comment -- otherwise,
                    //   we'd have a humongous homepage.
                    var today = new Date();
                    var comment_date = item.created;
                    // This could be off by a matter of hours, depending
                    //   on time zone, but that's not important.
                    if ((today - comment_date < days_to_show * MILLISECONDS_IN_DAY) ||
                            !days_to_show) {
                        $('#discussion-block').prepend(comment);
                    }
                    // Update the last fetched item ID each refresh to reduce return
                    last_update = item.id;
                });
            },
        });
        setTimeout(updateAllComments, timeout);
    }
    
    // Logic to get and display comments for a single piece.
    function updatePieceComments(piece, days_to_show) {
        $.ajax({
            type: "GET",
            url: "/comments/",
            cache: false,
            data: {
                'piece': piece,
                'last_update': last_update,
                },                    
            dataType: 'json',
            success: function (json) {
                $.each(json.results, function(i,item) {
                    if (piece == item.piece) {
                        var comment = '<div class="comment"><div class="author">' +
                            "<h5>" + item.author + 
                            "</a> &bull; " + item.created + '</h5></div>' +
                            '<div class="text"><p>' + parseCommentTags(item.text) +
                            '</p></div></div>';

                        // If we're in a context that limits number of comments,
                        //   check the date of the comment against the current date,
                        //   and only prepend if it's a recent comment -- otherwise,
                        //   we'd have a humongous homepage.
                        // NOTE: item.display_time is in _Python's_ date/time format,
                        //   and so JavaScript can't make use of its date/time functions.
                        //   Thus we import the string into JS format using Date.parse().
                        var today = new Date();
                        var comment_date = item.created;
                        // This could be off by a matter of hours, depending
                        //   on time zone, but that's not important.
                        if (today - comment_date < days_to_show * MILLISECONDS_IN_DAY) {
                            $('#discussion-block').prepend(comment);
                        }
                        else if (!days_to_show) {
                            // If showing all comments, order them first to last
                            $('#discussion-block').append(comment);
                        }
                        // Update the last fetched item ID each refresh to reduce return
                        last_update = item.id;
                    }
                });
            },
        });
        setTimeout(updatePieceComments, timeout);
    }
    
    function parseCommentTags(text) {
        return_text = "";
        text_array = text.split(" ");
        var text_array_len = text_array.length;
        var word = null;
        
        // Run through each word of the text looking for tags and replace them
        for (var i = 0; i < text_array_len; i++) {
            word = text_array[i];
            
            // @username replaced with link to profile page
            word = word.replace(/^@(.+)/gi,"<a href='/person/$1/'>@$1</a>");
            // DCxxxx replaced with link to piece page
            word = word.replace(/^#?DC(.+)/gi,"<a href='/piece/DC$1/'>DC$1</a>");
            // #piece replaced with link to piece page (just in case)
            word = word.replace(/^#(.+)/gi,"<a href='/piece/$1/'>#$1</a>");
            
            if (i != 0 ){ return_text = return_text + " "; }
            return_text = return_text + word;
        }
        return return_text;
    }
    
}

// Function to override normal form submission with an AJAX form submission
function attachCommentsAction () {
    $( "#comment-form" ).submit(function( event ){
        var form = $(this);
        $.ajax({
            type: "POST",
            url: "/comments/",
            data: form.serialize()
        });
        $( "#comment-form" ).reset()
        // testing needed
        $( "#see-comments" ).className += "in";
        event.preventDefault();
    });
}
