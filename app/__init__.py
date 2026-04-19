from flask import Flask
from app.config import get_config
from app.extensions import init_extensions, db
from app.routes import (
    auth_bp,
    procurement_bp,
    goods_receiving_bp,
    production_bp,
    packaging_bp,
    sales_bp,
    financial_bp
)


def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    init_extensions(app)
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(procurement_bp, url_prefix='/api/procurement')
    app.register_blueprint(goods_receiving_bp, url_prefix='/api/goods-receiving')
    app.register_blueprint(production_bp, url_prefix='/api/production')
    app.register_blueprint(packaging_bp, url_prefix='/api/packaging')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(financial_bp, url_prefix='/api/financial')
    
    @app.route('/')
    def index():
        return {
            'name': 'ERP System API',
            'version': '1.0.0',
            'status': 'running'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}
    
    return app
