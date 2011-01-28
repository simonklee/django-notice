var update = {
    url: null,
    target: null,

    poll: function() {
        $.ajax({
            url: update.url,
            async: true,
            cache: false,
            type: 'GET',
            dataType: 'json',
            timeout: 20000,
            success: update.onSuccess,
            error: update.onError,
        });
    },

    onSuccess: function(resp) {
        setTimeout(update.poll, 1); 
        for (var i = 0; i < resp.notices.length; i++) { 
            var node = $(document.createElement('li')).text(resp.notices[i]);
            node.hide()
            .appendTo(update.target)
            .fadeIn(400)
            .animate({
                opacity: 1.0
            }, 3000)
            .fadeOut("fast", function(){
                $(this).remove();
            });
        }
    },

    onError: function(resp) {
        console.log(resp);
        setTimeout(update.poll, 1);
    }
};

(function($) {
    $.fn.displayNotice = function(url, settings) {
        settings = $.extend({
        }, settings);

        return this.each(function() {
            update.target = $(this);
            update.url = url;
            setTimeout(update.poll, 1); // force async execution of code
        });
    };
})(jQuery);
