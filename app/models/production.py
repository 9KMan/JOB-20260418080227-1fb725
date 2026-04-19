from datetime import datetime
from app.extensions import db


class BillOfMaterials(db.Model):
    __tablename__ = 'bills_of_materials'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), unique=True, nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    version = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('BOMItem', back_populates='bom', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'product_code': self.product_code,
            'product_name': self.product_name,
            'description': self.description,
            'version': self.version,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items]
        }


class BOMItem(db.Model):
    __tablename__ = 'bom_items'

    id = db.Column(db.Integer, primary_key=True)
    bom_id = db.Column(db.Integer, db.ForeignKey('bills_of_materials.id'), nullable=False)
    component_name = db.Column(db.String(255), nullable=False)
    component_code = db.Column(db.String(50))
    quantity_required = db.Column(db.Numeric(10, 2), nullable=False)
    unit_of_measure = db.Column(db.String(20))

    bom = db.relationship('BillOfMaterials', back_populates='items')

    def to_dict(self):
        return {
            'id': self.id,
            'bom_id': self.bom_id,
            'component_name': self.component_name,
            'component_code': self.component_code,
            'quantity_required': float(self.quantity_required) if self.quantity_required else 0,
            'unit_of_measure': self.unit_of_measure
        }


class WorkOrder(db.Model):
    __tablename__ = 'work_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    bom_id = db.Column(db.Integer, db.ForeignKey('bills_of_materials.id'))
    product_name = db.Column(db.String(255), nullable=False)
    quantity_to_produce = db.Column(db.Numeric(10, 2), nullable=False)
    quantity_produced = db.Column(db.Numeric(10, 2), default=0)
    scheduled_start_date = db.Column(db.Date)
    scheduled_end_date = db.Column(db.Date)
    actual_start_date = db.Column(db.Date)
    actual_end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    operations = db.relationship('WorkOrderOperation', back_populates='work_order', cascade='all, delete-orphan')
    outputs = db.relationship('ProductionOutput', back_populates='work_order', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'bom_id': self.bom_id,
            'product_name': self.product_name,
            'quantity_to_produce': float(self.quantity_to_produce) if self.quantity_to_produce else 0,
            'quantity_produced': float(self.quantity_produced) if self.quantity_produced else 0,
            'scheduled_start_date': self.scheduled_start_date.isoformat() if self.scheduled_start_date else None,
            'scheduled_end_date': self.scheduled_end_date.isoformat() if self.scheduled_end_date else None,
            'actual_start_date': self.actual_start_date.isoformat() if self.actual_start_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'operations': [op.to_dict() for op in self.operations],
            'outputs': [out.to_dict() for out in self.outputs]
        }


class WorkOrderOperation(db.Model):
    __tablename__ = 'work_order_operations'

    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    operation_name = db.Column(db.String(255), nullable=False)
    operation_sequence = db.Column(db.Integer)
    workstation = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')
    notes = db.Column(db.Text)

    work_order = db.relationship('WorkOrder', back_populates='operations')

    def to_dict(self):
        return {
            'id': self.id,
            'work_order_id': self.work_order_id,
            'operation_name': self.operation_name,
            'operation_sequence': self.operation_sequence,
            'workstation': self.workstation,
            'status': self.status,
            'notes': self.notes
        }


class ProductionOutput(db.Model):
    __tablename__ = 'production_outputs'

    id = db.Column(db.Integer, primary_key=True)
    work_order_id = db.Column(db.Integer, db.ForeignKey('work_orders.id'), nullable=False)
    output_date = db.Column(db.Date, default=datetime.utcnow)
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    quality_status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    work_order = db.relationship('WorkOrder', back_populates='outputs')

    def to_dict(self):
        return {
            'id': self.id,
            'work_order_id': self.work_order_id,
            'output_date': self.output_date.isoformat() if self.output_date else None,
            'quantity': float(self.quantity) if self.quantity else 0,
            'quality_status': self.quality_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
