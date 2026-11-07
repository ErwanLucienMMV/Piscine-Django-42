"use strict";
$(function () {
    const scheme = location.protocol === "https:" ? "wss://" : "ws://";
    const socket = new WebSocket(scheme + location.host + $("#chat").attr("data-socket-path"));
    socket.addEventListener("open", function () {
        $("#connection-status").text("Connected");
        $("#message-form button").prop("disabled", false);
    });
    socket.addEventListener("message", function (event) {
        const data = JSON.parse(event.data);
        if (data.type === "message") {
            const line = $("<p>").addClass("message");
            $("<strong>").text(data.username + ": ").appendTo(line);
            $("<span>").text(data.text).appendTo(line);
            line.appendTo("#messages");
        } else if (data.type === "notice") {
            $("<p>").addClass("notice").text(data.text).appendTo("#messages");
        } else if (data.type === "error") {
            $("#chat-error").text(data.text);
        }
    });
    socket.addEventListener("close", function () {
        $("#connection-status").text("Disconnected. Refresh to reconnect, or log in again.");
        $("#message-form button").prop("disabled", true);
    });
    socket.addEventListener("error", function () { $("#chat-error").text("The connection failed."); });
    $("#message-form").on("submit", function (event) {
        event.preventDefault();
        if (socket.readyState !== WebSocket.OPEN) { return; }
        const text = $("#message").val();
        if (!text.trim()) { return; }
        socket.send(JSON.stringify({message: text}));
        $("#message").val("").trigger("focus");
        $("#chat-error").empty();
    });
    window.addEventListener("pagehide", function () { socket.close(); });
});
