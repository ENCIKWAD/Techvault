from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.catalog import catalog_bp
    from .routes.cart import cart_bp
    from .routes.order import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500

    return app
