from quart import Quart
from app.routes import setup_routes

def create_app():
    app = Quart(__name__)
    app.config['DEBUG'] = True

    # Setup routes
    setup_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()  # The default is localhost on port 5000