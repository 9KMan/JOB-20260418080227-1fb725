from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.production import BillOfMaterials, BOMItem, WorkOrder, WorkOrderOperation, ProductionOutput
from datetime import datetime
import uuid

production_bp = Blueprint('production', __name__)

def generate_work_order_number():
    return f"WO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"


@production_bp.route('/bom', methods=['GET'])
@jwt_required()
def get_boms():
    boms = BillOfMaterials.query.all()
    return jsonify([b.to_dict() for b in boms]), 200


@production_bp.route('/bom/<int:id>', methods=['GET'])
@jwt_required()
def get_bom(id):
    bom = BillOfMaterials.query.get(id)
    if not bom:
        return jsonify({'error': 'BOM not found'}), 404
    return jsonify(bom.to_dict()), 200


@production_bp.route('/bom', methods=['POST'])
@jwt_required()
def create_bom():
    data = request.get_json()
    
    bom = BillOfMaterials(
        product_code=data.get('product_code'),
        product_name=data.get('product_name'),
        description=data.get('description'),
        version=data.get('version', '1.0')
    )
    
    db.session.add(bom)
    db.session.flush()
    
    for item_data in data.get('items', []):
        item = BOMItem(
            bom_id=bom.id,
            component_name=item_data.get('component_name'),
            component_code=item_data.get('component_code'),
            quantity_required=item_data.get('quantity_required', 1),
            unit_of_measure=item_data.get('unit_of_measure')
        )
        db.session.add(item)
    
    db.session.commit()
    
    return jsonify(bom.to_dict()), 201


@production_bp.route('/work-orders', methods=['GET'])
@jwt_required()
def get_work_orders():
    orders = WorkOrder.query.all()
    return jsonify([o.to_dict() for o in orders]), 200


@production_bp.route('/work-orders/<int:id>', methods=['GET'])
@jwt_required()
def get_work_order(id):
    order = WorkOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Work order not found'}), 404
    return jsonify(order.to_dict()), 200


@production_bp.route('/work-orders', methods=['POST'])
@jwt_required()
def create_work_order():
    data = request.get_json()
    
    order = WorkOrder(
        order_number=generate_work_order_number(),
        bom_id=data.get('bom_id'),
        product_name=data.get('product_name'),
        quantity_to_produce=data.get('quantity_to_produce', 1),
        scheduled_start_date=data.get('scheduled_start_date'),
        scheduled_end_date=data.get('scheduled_end_date'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(order)
    db.session.flush()
    
    for op_data in data.get('operations', []):
        op = WorkOrderOperation(
            work_order_id=order.id,
            operation_name=op_data.get('operation_name'),
            operation_sequence=op_data.get('sequence'),
            workstation=op_data.get('workstation')
        )
        db.session.add(op)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 201


@production_bp.route('/work-orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_work_order(id):
    order = WorkOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Work order not found'}), 404
    
    data = request.get_json()
    
    order.status = data.get('status', order.status)
    order.quantity_produced = data.get('quantity_produced', order.quantity_produced)
    order.notes = data.get('notes', order.notes)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 200


@production_bp.route('/production-outputs', methods=['POST'])
@jwt_required()
def create_production_output():
    data = request.get_json()
    
    output = ProductionOutput(
        work_order_id=data.get('work_order_id'),
        quantity=data.get('quantity'),
        quality_status=data.get('quality_status'),
        notes=data.get('notes')
    )
    
    db.session.add(output)
    db.session.commit()
    
    return jsonify(output.to_dict()), 201
