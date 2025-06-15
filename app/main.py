from quart import Quart
from routes import setup_routes
from quart_cors import cors


def create_app():
    app = Quart(__name__)
    app.config['DEBUG'] = True
    cors(app, allow_origin="http://localhost:3000")

    # Setup routes
    setup_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()  # The default is localhost on port 5000