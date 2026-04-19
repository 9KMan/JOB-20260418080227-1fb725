from datetime import datetime
from app.extensions import db


class PackagingOrder(db.Model):
    __tablename__ = 'packaging_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'))
    packaging_date = db.Column(db.Date, default=datetime.utcnow)
    packed_by = db.Column(db.String(255))
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('PackagingOrderItem', back_populates='packaging_order', cascade='all, delete-orphan')
    labels = db.relationship('PackagingLabel', back_populates='packaging_order', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'sales_order_id': self.sales_order_id,
            'packaging_date': self.packaging_date.isoformat() if self.packaging_date else None,
            'packed_by': self.packed_by,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items],
            'labels': [label.to_dict() for label in self.labels]
        }


class PackagingOrderItem(db.Model):
    __tablename__ = 'packaging_order_items'

    id = db.Column(db.Integer, primary_key=True)
    packaging_order_id = db.Column(db.Integer, db.ForeignKey('packaging_orders.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    package_type = db.Column(db.String(50))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.Numeric(10, 2))

    packaging_order = db.relationship('PackagingOrder', back_populates='items')

    def to_dict(self):
        return {
            'id': self.id,
            'packaging_order_id': self.packaging_order_id,
            'product_name': self.product_name,
            'quantity': float(self.quantity) if self.quantity else 0,
            'package_type': self.package_type,
            'dimensions': self.dimensions,
            'weight': float(self.weight) if self.weight else 0
        }


class PackagingLabel(db.Model):
    __tablename__ = 'packaging_labels'

    id = db.Column(db.Integer, primary_key=True)
    packaging_order_id = db.Column(db.Integer, db.ForeignKey('packaging_orders.id'), nullable=False)
    label_number = db.Column(db.String(50), unique=True, nullable=False)
    barcode = db.Column(db.String(255))
    product_info = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    packaging_order = db.relationship('PackagingOrder', back_populates='labels')

    def to_dict(self):
        return {
            'id': self.id,
            'packaging_order_id': self.packaging_order_id,
            'label_number': self.label_number,
            'barcode': self.barcode,
            'product_info': self.product_info,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True)
    shipment_number = db.Column(db.String(50), unique=True, nullable=False)
    packaging_order_id = db.Column(db.Integer, db.ForeignKey('packaging_orders.id'))
    carrier = db.Column(db.String(100))
    tracking_number = db.Column(db.String(255))
    shipping_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'shipment_number': self.shipment_number,
            'packaging_order_id': self.packaging_order_id,
            'carrier': self.carrier,
            'tracking_number': self.tracking_number,
            'shipping_date': self.shipping_date.isoformat() if self.shipping_date else None,
            'delivery_date': self.delivery_date.isoformat() if self.delivery_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
