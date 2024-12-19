$(document).on('click', '.like-button', function(e) {
    e.preventDefault(); 
    var post_id = $(this).data('post'); 
    var liked = $(this).data('liked'); 
    var url = liked ? '/remove_like_post/' + post_id + '/' : '/like_post/' + post_id + '/';

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            var button = $('#post-' + post_id + ' .like-button');
            var icon = button.find('i'); 
            var likeMessage = $('#post-' + post_id + ' .like-message');
            button.data('liked', !liked); 

            
            icon.toggleClass('bi-heart-fill text-danger bi-heart');

            var likes = response.likes;
            
            $('#post-' + post_id + ' .like-count').text(likes);
            
            updateLikeMessage(likeMessage, likes, !liked); 
        },
        error: function(xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText); 
        }
    });
});


function updateLikeMessage(element, likes, liked) {
    if (likes === 0) {
        element.text('Be the first to like this');
    } else if (likes === 1) {
        element.text(liked ? 'You liked this' : '1 person liked this');
    } else {
        element.text(liked ? `You and ${likes - 1} others liked this` : `${likes} people liked this`);
    }
}
