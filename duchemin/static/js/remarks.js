function editRemarksAction() {
    $('.open-EditRemarks').on({
        'click': function(event) {
            var personid = $(this).data('personid');

            $.ajax({
                type: "GET",
                url: "/person/" + personid,
                dataType: 'json',
                success: function (json) {
                    showRemarksModalAction(personid, json.remarks);
                },
                error: function () {
                    showRemarksModalAction(personid);
                }
            });

            return false;
        }
    });
}


function showRemarksModalAction(personid, remarkstext) {
    // Remove old modal, if any
    $("#editRemarks").remove();

    // Title string
    var titletext = ('Edit Public Profile');
    var remarkstext = '';

    // Outer div for modal.
    var modal = $("<div />", {
        "id": "editRemarks",
        "class": "modal fade",
        "tabindex": "-1",
        "role": "dialog",
        "aria-labelledby": "editRemarks",
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
        "id": "editRemarksLabel",
        "text": titletext,
    }).appendTo(modal_header);

    // Modal body div
    var modal_body = $("<div />", {
        "class": "modal-body",
    }).appendTo(modal_content);

    // Modal body: paragraph
    var modal_body_p = $("<p />", {
        "id": "modal-body-p",
    }).appendTo(modal_body);

    // Modal body: form's person ID
    var modal_body_personid = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "person_id",
        "id": "person-id",
        "value": personid,
    }).appendTo(modal_body_p);

    // Modal body: form's textarea
    var modal_body_textarea = $("<textarea />", {
        "form": "modal-form",
        "name": "text",
        "rows": "10",
        "id": "remarks-textarea",
        "style": "width:100%; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;",
        "text": remarkstext,
    }).appendTo(modal_body_p);

    // Modal footer div
    var modal_footer = $("<div />", {
        "class": "modal-footer",
    }).appendTo(modal_content);

    // Only show button to delete if there was a remarks there in the first place
    if (remarkstext != '') {
        var modal_footer_delete = $("<button />", {
            "type": "button",
            "id": "modal-delete",
            "class": "btn btn-danger pull-left",
            "data-dismiss": "modal",
            "text": "Delete",
        }).appendTo(modal_footer);
    }

    // Modal footer: close
    var modal_footer_close = $("<button />", {
        "type": "button",
        "class": "btn",
        "data-dismiss": "modal",
        "text": "Close",
    }).appendTo(modal_footer);

    // Modal footer: save
    var modal_footer_save = $("<button />", {
        "form": "modal-form",
        "type": "submit",
        "id": "modal-save",
        "class": "btn btn-success",
        "data-dismiss": "modal",
        "text": "Save changes",
    }).appendTo(modal_footer);

    $("#editRemarks").modal({
        "backdrop": "static",
    });

    $( "#modal-save" ).on({
        'click': function(event) {
            $('#modal-form').submit();
            event.preventDefault();
        }
    });

    $( "#modal-delete" ).on({
        'click': function(event) {
            confirmDeleteRemarksAction(personid);
        }
    });
}

function submitRemarksAction() {
    $( "#modal-form" ).submit(function( event ){
        var form = $(this);
        var serialized_data = form.serialize();
        $.ajax({
            type: "POST",
            url: "/person/",
            data: serialized_data,
        });

        // If it was an Add Remarks button, make it now an Edit Remarks button
        var button = document.getElementById("button-remarks");
        if (button) {
            button.innerHTML = "Edit Public Profile";
            button.title = "Edit Public Profile";
        }
        event.preventDefault();
    });
}

function confirmDeleteRemarksAction(personid, remarkstext) {
    // Remove old modal, if any
    $("#confirmDelete").remove();

    // Title string
    var titletext = ('Delete Remarks');

    // Outer div for modal.
    var modal = $("<div />", {
        "id": "confirmDelete",
        "class": "modal fade",
        "tabindex": "-1",
        "role": "dialog",
        "aria-labelledby": "confirmDelete",
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
        "id": "confirmDeleteLabel",
        "text": titletext,
    }).appendTo(modal_header);

    // Modal body div
    var modal_body = $("<div />", {
        "class": "modal-body",
    }).appendTo(modal_content);

    // Modal body: paragraph
    var modal_body_p = $("<p />", {
        "id": "modal-body-p",
        "text": "Are you sure you want to delete your public profile?",
    }).appendTo(modal_body);

    // Modal body: form's person ID
    // Still needed?
    var modal_body_personid = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "person_id",
        "id": "person-id",
        "value": personid,
    }).appendTo(modal_body_p);

    // Modal body: new text of the public profile, which is empty,
    // because we're deleting it
    var modal_body_personid = $("<input />", {
        "form": "modal-form",
        "type": "hidden",
        "name": "text",
        "id": "text",
        "value": '',
    }).appendTo(modal_body_p);

    // Modal footer div
    var modal_footer = $("<div />", {
        "class": "modal-footer",
    }).appendTo(modal_content);

    var modal_footer_cancel = $("<button />", {
        "type": "button",
        "id": "cancel-delete",
        "class": "btn",
        "data-dismiss": "modal",
        "data-personid": personid,
        "text": "Cancel",
    }).appendTo(modal_footer);

    var modal_footer_delete = $("<button />", {
        "form": "modal-form",
        "type": "submit",
        "id": "confirm-delete",
        "class": "btn btn-danger",
        "data-dismiss": "modal",
        "text": "Delete",
    }).appendTo(modal_footer);

    $("#confirmDelete").modal({
        "backdrop": "static",
    });

    $( "#cancel-delete" ).on({
        'click': function(event) {
            showRemarksModalAction(personid, remarkstext);
        }
    });

    $( "#confirm-delete" ).on({
        'click': function(event) {
            $('#modal-form').submit();

            // If it was an Edit Remarks button, make it now an Add Remarks button
            var button = document.getElementById("button-remarks");
            if (button) {
                button_fav.innerHTML = "Add Public Profile";
                button_fav.title = "Add Public Profile";
            }
            event.preventDefault();
        }
    });
}
