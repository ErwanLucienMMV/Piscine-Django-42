"use strict";
$(function () {
    const scheme = location.protocol === "https:" ? "wss://" : "ws://";
    const socket = new WebSocket(scheme + location.host + $("#chat").attr("data-socket-path"));
    function appendMessage(data) {
        const line = $("<p>").addClass("message");
        $("<strong>").text(data.username + ": ").appendTo(line);
        $("<span>").text(data.text).appendTo(line);
        line.appendTo("#messages");
    }
    function scrollToBottom() {
        const messages = $("#messages")[0];
        messages.scrollTop = messages.scrollHeight;
    }
    socket.addEventListener("open", function () {
        $("#connection-status").text("Connected");
        $("#message-form button").prop("disabled", false);
    });
    socket.addEventListener("message", function (event) {
        const data = JSON.parse(event.data);
        if (data.type === "message") {
            appendMessage(data);
        } else if (data.type === "history") {
            data.messages.forEach(appendMessage);
        } else if (data.type === "notice") {
            $("<p>").addClass("notice").text(data.text).appendTo("#messages");
            $("#users").empty();
            data.users.forEach(function (username) { $("<li>").text(username).appendTo("#users"); });
        } else if (data.type === "error") {
            $("#chat-error").text(data.text);
        }
        scrollToBottom();
    });
    socket.addEventListener("close", function () {
        $("#connection-status").text("Disconnected. Refresh to reconnect, or log in again.");
        $("#message-form button").prop("disabled", true);
        $("#users").empty();
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
