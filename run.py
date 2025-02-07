from app.database import create_app, socketio

app = create_app()

if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()  # ✅ Ensure eventlet is patched correctly

    # ✅ Force WebSockets instead of polling
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
