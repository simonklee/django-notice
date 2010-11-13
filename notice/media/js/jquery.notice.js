(function($) {
    $.fn.displayNotice = function(url, settings) {
        settings = $.extend({
            callback: false
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
                    status = data.valid;
                    console.log("request was " + status);
                    if (status) {
                        if (settings.callback)  {
                            settings.callback(data);
                        } else {
                            console.log("got notices ");
                            $.each(data.notices, function(k, v) {
                                console.log("notices " + k + " " + v);
                                $('<p>' + v + '</p>').appendTo(target);
                            });
                        }
                    }
                },
                type: 'GET',
                url: url
            });
            return status;
        });
    };
})(jQuery);
