from chatbot import ChatBot

# Try to import Flask; if unavailable or incompatible, fail gracefully so the module
# can still be imported in environments without Flask/Jinja2 installed.
try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
    _import_error = None
except Exception as e:
    Flask = None
    FLASK_AVAILABLE = False
    _import_error = e

bot = ChatBot()

if FLASK_AVAILABLE:
    app = Flask(__name__, template_folder="templates")

    @app.route('/')
    def index():
        return render_template('index.html', bot_name=bot.name)

    @app.route('/api/message', methods=['POST'])
    def message():
        data = request.get_json(silent=True) or {}
        text = data.get('message') if isinstance(data, dict) else None
        if text is None:
            text = request.form.get('message')
        if not text:
            return jsonify({'error': 'no message provided'}), 400
        reply = bot.respond(text)
        return jsonify({'reply': reply})

    if __name__ == '__main__':
        # For development only. Use a proper WSGI server for production.
        app.run(debug=True, host='127.0.0.1', port=5000)
else:
    app = None

    def message():
        raise RuntimeError(f"Flask (or its dependencies) are not available: {_import_error}")

    if __name__ == '__main__':
        print('Cannot start web server — Flask or dependencies unavailable:')
        print(_import_error)
