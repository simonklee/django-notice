(function($) {
    var onSuccess = function(data, target) {
        var status = data.valid;
        //console.log("request was " + status);
        if (status) {
            // console.log("got notices ");
            $.each(data.notices, function(k, v) {
                $('<p class="notice">' + v + '</p>')
                    .hide()
                    .appendTo(target)
                    .fadeIn(400)
                    .animate({
                        opacity: 1.0
                    }, 3000)
                    .fadeOut("fast", function(){
  					    $(this).remove();
                    });
            });
        }
    }

    $.fn.displayNotice = function(url, settings) {
        settings = $.extend({
            callback: onSuccess
        }, settings);

        return this.each(function() {
            var target = $(this);
            var status = false;
            
            $.ajax({
                dataType: 'json',
                error: function(XHR, textStatus, errorThrown)   {
                    status = false;
                    console.log("request was " + errorThrown);
                },
                success: function(data) {
                    settings.callback(data, target);
                },
                type: 'GET',
                url: url
            });
            return status;
        });
    };
})(jQuery);
