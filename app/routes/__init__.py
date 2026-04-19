from app.routes.auth import auth_bp
from app.routes.procurement import procurement_bp
from app.routes.goods_receiving import goods_receiving_bp
from app.routes.production import production_bp
from app.routes.packaging import packaging_bp
from app.routes.sales import sales_bp
from app.routes.financial import financial_bp

__all__ = [
    'auth_bp',
    'procurement_bp',
    'goods_receiving_bp',
    'production_bp',
    'packaging_bp',
    'sales_bp',
    'financial_bp'
]
