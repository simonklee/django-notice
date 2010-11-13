(function($) {
    $.fn.displayMessages = function(url, settings) {
        settings = $.extend({
            all: true
        }, settings);

        return this.each(function() {
            var target = $(this);
                $.ajax({
                    async: false,
                    dataType: 'json',
                    traditional: true,
                    error: function(XHR, textStatus, errorThrown)   {
                        status = true;
                    },
                    success: function(data, textStatus) {
                        status = data.valid;
                        if (!status)    {
                            if (settings.callback)  {
                                settings.callback(data, form);
                            }
                        }
                    },
                    type: 'GET',
                    url: url
                });
                return status;
            });
        });
    };
})(jQuery);
