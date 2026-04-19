from datetime import datetime
from app.extensions import db


class GoodsReceivedNote(db.Model):
    __tablename__ = 'goods_received_notes'

    id = db.Column(db.Integer, primary_key=True)
    grn_number = db.Column(db.String(50), unique=True, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'))
    received_date = db.Column(db.Date, default=datetime.utcnow)
    received_by = db.Column(db.String(255))
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('GRNLineItem', back_populates='grn', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'grn_number': self.grn_number,
            'purchase_order_id': self.purchase_order_id,
            'received_date': self.received_date.isoformat() if self.received_date else None,
            'received_by': self.received_by,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items]
        }


class GRNLineItem(db.Model):
    __tablename__ = 'grn_line_items'

    id = db.Column(db.Integer, primary_key=True)
    grn_id = db.Column(db.Integer, db.ForeignKey('goods_received_notes.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    expected_quantity = db.Column(db.Numeric(10, 2), nullable=False)
    received_quantity = db.Column(db.Numeric(10, 2), nullable=False)
    accepted_quantity = db.Column(db.Numeric(10, 2))
    rejected_quantity = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)

    grn = db.relationship('GoodsReceivedNote', back_populates='items')

    def to_dict(self):
        return {
            'id': self.id,
            'grn_id': self.grn_id,
            'product_name': self.product_name,
            'expected_quantity': float(self.expected_quantity) if self.expected_quantity else 0,
            'received_quantity': float(self.received_quantity) if self.received_quantity else 0,
            'accepted_quantity': float(self.accepted_quantity) if self.accepted_quantity else 0,
            'rejected_quantity': float(self.rejected_quantity) if self.rejected_quantity else 0,
            'notes': self.notes
        }


class QualityCheck(db.Model):
    __tablename__ = 'quality_checks'

    id = db.Column(db.Integer, primary_key=True)
    grn_id = db.Column(db.Integer, db.ForeignKey('goods_received_notes.id'), nullable=False)
    inspector_name = db.Column(db.String(255))
    inspection_date = db.Column(db.Date, default=datetime.utcnow)
    result = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'grn_id': self.grn_id,
            'inspector_name': self.inspector_name,
            'inspection_date': self.inspection_date.isoformat() if self.inspection_date else None,
            'result': self.result,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
