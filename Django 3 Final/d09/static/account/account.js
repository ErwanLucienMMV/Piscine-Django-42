"use strict";
$(function () {
    $("#login-form, #logout-form").on("submit", function (event) {
        event.preventDefault();
        const form = $(this);
        const action = this.id === "login-form" ? "login" : "logout";
        const button = form.find("button").prop("disabled", true);
        $("#account-errors").empty();
        $.ajax({
            url: form.attr("action"),
            method: "POST",
            data: form.serialize() + "&action=" + action,
            dataType: "json"
        }).done(function (data) {
            $("input[name=csrfmiddlewaretoken]").val(data.csrfToken);
            $("#username").text(data.username);
            $("#login-panel").prop("hidden", data.authenticated);
            $("#logged-panel").prop("hidden", !data.authenticated);
            $("#id_password").val("");
        }).fail(function (xhr) {
            const errors = xhr.responseJSON && xhr.responseJSON.errors;
            if (errors) {
                $.each(errors, function (field, items) {
                    items.forEach(function (item) {
                        $("<p>").text((field === "__all__" ? "" : field + ": ") + item.message)
                            .appendTo("#account-errors");
                    });
                });
            } else {
                $("#account-errors").text("The request failed. Please refresh the page and try again.");
            }
        }).always(function () { button.prop("disabled", false); });
    });
});
