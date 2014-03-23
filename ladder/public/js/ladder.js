$(document).ready( function () {
    "use strict";

    function bindTicketRequestPreview() {
        $("textarea#id_message").bind("input propertychange", function(e) {
            var message = $(this).val();
            // update visibility.
            if ( !_.isEmpty(message) ) {
                $("#message-preview").show()
            } else {
                $("#message-preview").hide()
            }
            // update the preview.
            $("#message-body").text(message);
        })
        $("textarea#id_message").trigger("propertychange");
    }

    bindTicketRequestPreview();
});
