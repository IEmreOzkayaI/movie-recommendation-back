from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=3001, use_reloader=False, use_debugger=False)
