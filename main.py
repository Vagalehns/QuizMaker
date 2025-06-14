from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session security in SocketIO
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
    
@socketio.on('message')
def handle_message(msg):
    with open("test.txt", "w") as f:
        f.write(msg)
    print(f"Received message: {msg}")


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)



