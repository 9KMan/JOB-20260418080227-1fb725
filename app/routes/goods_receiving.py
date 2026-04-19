from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.goods_receiving import GoodsReceivedNote, GRNLineItem, QualityCheck
from datetime import datetime
import uuid

goods_receiving_bp = Blueprint('goods_receiving', __name__)

def generate_grn_number():
    return f"GRN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"


@goods_receiving_bp.route('/grn', methods=['GET'])
@jwt_required()
def get_grns():
    grns = GoodsReceivedNote.query.all()
    return jsonify([g.to_dict() for g in grns]), 200


@goods_receiving_bp.route('/grn/<int:id>', methods=['GET'])
@jwt_required()
def get_grn(id):
    grn = GoodsReceivedNote.query.get(id)
    if not grn:
        return jsonify({'error': 'GRN not found'}), 404
    return jsonify(grn.to_dict()), 200


@goods_receiving_bp.route('/grn', methods=['POST'])
@jwt_required()
def create_grn():
    data = request.get_json()
    
    grn = GoodsReceivedNote(
        grn_number=generate_grn_number(),
        purchase_order_id=data.get('purchase_order_id'),
        received_by=data.get('received_by'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(grn)
    db.session.flush()
    
    for item_data in data.get('items', []):
        item = GRNLineItem(
            grn_id=grn.id,
            product_name=item_data.get('product_name'),
            expected_quantity=item_data.get('expected_quantity', 0),
            received_quantity=item_data.get('received_quantity', 0),
            accepted_quantity=item_data.get('received_quantity', 0),
            notes=item_data.get('notes')
        )
        db.session.add(item)
    
    db.session.commit()
    
    return jsonify(grn.to_dict()), 201


@goods_receiving_bp.route('/grn/<int:id>', methods=['PUT'])
@jwt_required()
def update_grn(id):
    grn = GoodsReceivedNote.query.get(id)
    if not grn:
        return jsonify({'error': 'GRN not found'}), 404
    
    data = request.get_json()
    
    grn.status = data.get('status', grn.status)
    grn.notes = data.get('notes', grn.notes)
    
    db.session.commit()
    
    return jsonify(grn.to_dict()), 200


@goods_receiving_bp.route('/quality-checks', methods=['GET'])
@jwt_required()
def get_quality_checks():
    checks = QualityCheck.query.all()
    return jsonify([c.to_dict() for c in checks]), 200


@goods_receiving_bp.route('/quality-checks', methods=['POST'])
@jwt_required()
def create_quality_check():
    data = request.get_json()
    
    check = QualityCheck(
        grn_id=data.get('grn_id'),
        inspector_name=data.get('inspector_name'),
        result=data.get('result'),
        notes=data.get('notes')
    )
    
    db.session.add(check)
    db.session.commit()
    
    return jsonify(check.to_dict()), 201
