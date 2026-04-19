from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.packaging import PackagingOrder, PackagingOrderItem, PackagingLabel, Shipment
from datetime import datetime
import uuid

packaging_bp = Blueprint('packaging', __name__)

def generate_packaging_number():
    return f"PKG-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

def generate_shipment_number():
    return f"SHP-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

def generate_label_number():
    return f"LBL-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"


@packaging_bp.route('/packaging-orders', methods=['GET'])
@jwt_required()
def get_packaging_orders():
    orders = PackagingOrder.query.all()
    return jsonify([o.to_dict() for o in orders]), 200


@packaging_bp.route('/packaging-orders/<int:id>', methods=['GET'])
@jwt_required()
def get_packaging_order(id):
    order = PackagingOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Packaging order not found'}), 404
    return jsonify(order.to_dict()), 200


@packaging_bp.route('/packaging-orders', methods=['POST'])
@jwt_required()
def create_packaging_order():
    data = request.get_json()
    
    order = PackagingOrder(
        order_number=generate_packaging_number(),
        sales_order_id=data.get('sales_order_id'),
        packed_by=data.get('packed_by'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(order)
    db.session.flush()
    
    for item_data in data.get('items', []):
        item = PackagingOrderItem(
            packaging_order_id=order.id,
            product_name=item_data.get('product_name'),
            quantity=item_data.get('quantity', 1),
            package_type=item_data.get('package_type'),
            dimensions=item_data.get('dimensions'),
            weight=item_data.get('weight')
        )
        db.session.add(item)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 201


@packaging_bp.route('/packaging-orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_packaging_order(id):
    order = PackagingOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Packaging order not found'}), 404
    
    data = request.get_json()
    order.status = data.get('status', order.status)
    order.notes = data.get('notes', order.notes)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 200


@packaging_bp.route('/labels', methods=['GET'])
@jwt_required()
def get_labels():
    labels = PackagingLabel.query.all()
    return jsonify([l.to_dict() for l in labels]), 200


@packaging_bp.route('/labels', methods=['POST'])
@jwt_required()
def create_label():
    data = request.get_json()
    
    label = PackagingLabel(
        packaging_order_id=data.get('packaging_order_id'),
        label_number=generate_label_number(),
        barcode=data.get('barcode'),
        product_info=data.get('product_info')
    )
    
    db.session.add(label)
    db.session.commit()
    
    return jsonify(label.to_dict()), 201


@packaging_bp.route('/shipments', methods=['GET'])
@jwt_required()
def get_shipments():
    shipments = Shipment.query.all()
    return jsonify([s.to_dict() for s in shipments]), 200


@packaging_bp.route('/shipments/<int:id>', methods=['GET'])
@jwt_required()
def get_shipment(id):
    shipment = Shipment.query.get(id)
    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404
    return jsonify(shipment.to_dict()), 200


@packaging_bp.route('/shipments', methods=['POST'])
@jwt_required()
def create_shipment():
    data = request.get_json()
    
    shipment = Shipment(
        shipment_number=generate_shipment_number(),
        packaging_order_id=data.get('packaging_order_id'),
        carrier=data.get('carrier'),
        tracking_number=data.get('tracking_number'),
        shipping_date=data.get('shipping_date'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(shipment)
    db.session.commit()
    
    return jsonify(shipment.to_dict()), 201


@packaging_bp.route('/shipments/<int:id>', methods=['PUT'])
@jwt_required()
def update_shipment(id):
    shipment = Shipment.query.get(id)
    if not shipment:
        return jsonify({'error': 'Shipment not found'}), 404
    
    data = request.get_json()
    shipment.status = data.get('status', shipment.status)
    shipment.tracking_number = data.get('tracking_number', shipment.tracking_number)
    shipment.delivery_date = data.get('delivery_date', shipment.delivery_date)
    shipment.notes = data.get('notes', shipment.notes)
    
    db.session.commit()
    
    return jsonify(shipment.to_dict()), 200
