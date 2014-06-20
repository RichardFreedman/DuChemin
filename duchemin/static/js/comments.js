// Helper function to start appropriate timeout loop for comments feed
function startCommentFeed(piece_id){

    // First fetch has id 0, so it gets everything
    var last_update = 0;
    var timeout = 2000;
    
    // Check to see if the helper function was called with a piece_id or not
    if (piece_id != null){
    	updatePieceComments(piece_id);
    } else {
    	updateAllComments();
    }

    // Logic to handle getting and displaying all comments
    function updateAllComments() {
        $.ajax({
            type: "GET",
            url: "/discussion/",
            cache: false,
            data: {
                'last_update': last_update,
                },             
            dataType: 'json',
            success: function (json) {
                $.each(json, function(i,item) {
                    // Isn't there any way to get the full name, such as
                    // `item.author.first_name + item.author.last_name` ?
                    // I thought item.author was of the User model.

                    // Also, I surrounded the comments in a <p> element,
                    // which should be fine. Without it, the margins are
                    // terrible. Another way to do it might be to modify
                    // the CSS to add margin to .comment blocks.
                    var comment = '<div class="comment"><div class="author">' +
                        "<h4><a href='/piece/" + item.piece_id + "'>" +
                        item.piece_id + "</a> &bull; <a href='/person/" +
                        item.author + "'>" + item.author + 
                        "</a> &bull; " + item.display_time + '</h4></div>' +
                        '<div class="text"><p>' + parseCommentTags(item.text) +
                        '</p></div></div>';

                    $('#discussion-block').prepend(comment);
                    // Update the last fetched item ID each refresh to reduce return
                    last_update = item.id;
                });
            },
        });
        setTimeout(updateAllComments, timeout);
    }
    
    function updatePieceComments(piece_id) {
        $.ajax({
            type: "GET",
            url: "/discussion/",
            cache: false,
            data: {
                'piece_id': piece_id,
                'last_update': last_update,
                },                    
            dataType: 'json',
            success: function (json) {
                $.each(json, function(i,item) {

                    //TODO: Make this prettier
                    var comment = '<div class="comment"><div class="author">'
                        + item.author + ": " + item.display_time
                        + '</div><div class="text">' + parseCommentTags(item.text)
                        + '</div>';

                    $('#discussion-block').prepend(comment);
                    // Update the last fetched item ID each refresh to reduce return
                    last_update = item.id;
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
            // #piece replaced with link to piece page
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
        	url: "/discussion/",
        	data: form.serialize()
        });
        event.preventDefault();
    });
}