function log(msg) {
    setTimeout(function() {
        throw new Error(msg);
    }, 0);
}

function attachNoteAction() {
    $( "#note-form" ).submit(function( event ){
        var form = $(this);
        $.ajax({
            type: "POST",
            url: "/notes/",
            data: form.serialize(),
            success: function (json) {
                $('#editNote').modal('hide');
            },
        });
        event.preventDefault();
    });
}

function editNoteAction() {
    $('.open-EditNote').on({
        'click': function(event) {
            // Remove old modal, if any
            $("#editNote").remove();

            // Title string
            var title_text = ('Edit Note to Piece ' + $(this).data('pieceid'));

            // Outer div for modal.
            var modal = $("<div />", {
                "id": "editNote",
                "class": "modal fade",
                "tabindex": "-1",
                "role": "dialog",
                "aria-labelledby": "editNote",
                "aria-hidden": "true",
            }).appendTo("body");

            // First layer div
            var modal_dialog = $("<div />", {
                "class": "modal-dialog",
            }).appendTo(modal);

            // Second layer div
            var modal_content = $("<div />", {
                "class": "modal-content",
            }).appendTo(modal_dialog);

            // Modal header div
            var modal_header = $("<div />", {
                "class": "modal-header",
            }).appendTo(modal_content);

            // Modal header: button
            var modal_header_button = $("<button />", {
                "type": "button",
                "class": "close",
                "data-dismiss": "modal",
                "aria-hidden": "true",
                "text": "×",
            }).appendTo(modal_header);

            // Modal header: text
            var modal_header_text = $("<h3 />", {
                "class": "modal-title",
                "id": "editNoteLabel",
                "text": title_text,
            }).appendTo(modal_header);

            // Modal body div
            var modal_body = $("<div />", {
                "class": "modal-body",
            }).appendTo(modal_content);

            // Modal body: paragraph
            var modal_body_p = $("<p />", {
                "id": "modal-body-p",
            }).appendTo(modal_body);

            // Modal body: textarea
            var modal_body_p_textarea = $("<textarea />", {
                "form": "note-form",
                "name": ("Type a Note to Piece " + $(".open-EditNote").data('pieceid')),
                "rows": "10",
                "id": "note-form",
                "style": "width:100%; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;",
                "text": $(this).data('notetext'),
            }).appendTo(modal_body_p);

            // Modal footer div
            var modal_footer = $("<div />", {
                "class": "modal-footer",
            }).appendTo(modal_content);

            var modal_footer_close = $("<button />", {
                "type": "button",
                "class": "btn btn-default",
                "data-dismiss": "modal",
                "text": "Close",
            }).appendTo(modal_footer);

            var modal_footer_save = $("<button />", {
                "type": "button",
                "class": "btn btn-primary",
                "text": "Save changes",
            }).appendTo(modal_footer);

            $("#editNote").modal({
                "backdrop": "static",
            });

            return false;
        }
    });
}

