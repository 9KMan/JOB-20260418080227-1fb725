from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.procurement import Supplier, PurchaseOrder, PurchaseOrderItem, PurchaseRequisition
from datetime import datetime
import uuid

procurement_bp = Blueprint('procurement', __name__)

def generate_order_number():
    return f"PO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

def generate_requisition_number():
    return f"PR-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"


@procurement_bp.route('/suppliers', methods=['GET'])
@jwt_required()
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([s.to_dict() for s in suppliers]), 200


@procurement_bp.route('/suppliers/<int:id>', methods=['GET'])
@jwt_required()
def get_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    return jsonify(supplier.to_dict()), 200


@procurement_bp.route('/suppliers', methods=['POST'])
@jwt_required()
def create_supplier():
    data = request.get_json()
    
    supplier = Supplier(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address')
    )
    
    db.session.add(supplier)
    db.session.commit()
    
    return jsonify(supplier.to_dict()), 201


@procurement_bp.route('/suppliers/<int:id>', methods=['PUT'])
@jwt_required()
def update_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    
    data = request.get_json()
    
    supplier.name = data.get('name', supplier.name)
    supplier.email = data.get('email', supplier.email)
    supplier.phone = data.get('phone', supplier.phone)
    supplier.address = data.get('address', supplier.address)
    supplier.is_active = data.get('is_active', supplier.is_active)
    
    db.session.commit()
    
    return jsonify(supplier.to_dict()), 200


@procurement_bp.route('/suppliers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    
    db.session.delete(supplier)
    db.session.commit()
    
    return jsonify({'message': 'Supplier deleted'}), 200


@procurement_bp.route('/purchase-orders', methods=['GET'])
@jwt_required()
def get_purchase_orders():
    orders = PurchaseOrder.query.all()
    return jsonify([o.to_dict() for o in orders]), 200


@procurement_bp.route('/purchase-orders/<int:id>', methods=['GET'])
@jwt_required()
def get_purchase_order(id):
    order = PurchaseOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Purchase order not found'}), 404
    return jsonify(order.to_dict()), 200


@procurement_bp.route('/purchase-orders', methods=['POST'])
@jwt_required()
def create_purchase_order():
    data = request.get_json()
    
    order = PurchaseOrder(
        supplier_id=data.get('supplier_id'),
        order_number=generate_order_number(),
        expected_date=data.get('expected_date'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(order)
    db.session.flush()
    
    total = 0
    for item_data in data.get('items', []):
        item = PurchaseOrderItem(
            purchase_order_id=order.id,
            product_name=item_data.get('product_name'),
            description=item_data.get('description'),
            quantity=item_data.get('quantity', 1),
            unit_price=item_data.get('unit_price', 0),
            total_price=item_data.get('quantity', 1) * item_data.get('unit_price', 0)
        )
        total += item.total_price
        db.session.add(item)
    
    order.total_amount = total
    db.session.commit()
    
    return jsonify(order.to_dict()), 201


@procurement_bp.route('/purchase-orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_purchase_order(id):
    order = PurchaseOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    data = request.get_json()
    
    order.status = data.get('status', order.status)
    order.notes = data.get('notes', order.notes)
    order.expected_date = data.get('expected_date', order.expected_date)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 200


@procurement_bp.route('/purchase-requisitions', methods=['GET'])
@jwt_required()
def get_purchase_requisitions():
    requisitions = PurchaseRequisition.query.all()
    return jsonify([r.to_dict() for r in requisitions]), 200


@procurement_bp.route('/purchase-requisitions', methods=['POST'])
@jwt_required()
def create_purchase_requisition():
    data = request.get_json()
    
    requisition = PurchaseRequisition(
        request_number=generate_requisition_number(),
        department=data.get('department'),
        requested_by=data.get('requested_by'),
        items=data.get('items'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(requisition)
    db.session.commit()
    
    return jsonify(requisition.to_dict()), 201
