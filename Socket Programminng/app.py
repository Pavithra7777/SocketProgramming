from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config["SECRET_KEY"] = "socket-chat-secret"

socketio = SocketIO(app)


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("join")
def handle_join(username):

    print(f"{username} joined the chat")

    emit(
        "system_message",
        f"{username} joined the chat",
        broadcast=True
    )


@socketio.on("chat_message")
def handle_message(data):

    username = data["username"]
    message = data["message"]

    print(f"{username}: {message}")

    # Send message to everyone
    emit(
        "chat_message",
        {
            "username": username,
            "message": message
        },
        broadcast=True
    )


if __name__ == "__main__":

    print("--------------------------------")
    print("       SOCKET CHAT SERVER")
    print("--------------------------------")
    print("Server running on port 5000")
    print("--------------------------------")

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )