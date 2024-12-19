$(document).on('click', '.like-button', function(e) {
    e.preventDefault(); // Evita el comportamiento predeterminado del botón
    var post_id = $(this).data('post'); // Obtiene el ID del post
    var liked = $(this).data('liked'); // Obtiene el estado actual de "liked"
    var url = liked ? '/remove_like_post/' + post_id + '/' : '/give_like_post/' + post_id + '/';

    $.ajax({
        type: 'GET',
        url: url,
        success: function(response) {
            var button = $('#post-' + post_id + ' .like-button');
            var icon = button.find('i'); // Selecciona el icono dentro del botón
            var likeMessage = $('#post-' + post_id + ' .like-message');
            button.data('liked', !liked); // Cambia el estado de "liked"

            // Actualiza el icono
            icon.toggleClass('bi-heart-fill text-danger bi-heart');

            var likes = response.likes;
            // Actualiza el contador de likes
            $('#post-' + post_id + ' .like-count').text(likes);
            // Actualiza el mensaje de "likes"
            updateLikeMessage(likeMessage, likes, !liked); // Pasamos !liked ya que el estado ha cambiado
        },
        error: function(xhr, errmsg, err) {
            console.error(xhr.status + ": " + xhr.responseText); // Muestra un mensaje de error en la consola
        }
    });
});

// Función para actualizar el mensaje de "likes"
function updateLikeMessage(element, likes, liked) {
    if (likes === 0) {
        element.text('Be the first to like this');
    } else if (likes === 1) {
        element.text(liked ? 'You liked this' : '1 person liked this');
    } else {
        element.text(liked ? `You and ${likes - 1} others liked this` : `${likes} people liked this`);
    }
}
