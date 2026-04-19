from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.sales import Customer, SalesOrder, SalesOrderItem, Invoice
from datetime import datetime
import uuid

sales_bp = Blueprint('sales', __name__)

def generate_order_number():
    return f"SO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

def generate_invoice_number():
    return f"INV-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"


@sales_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers]), 200


@sales_bp.route('/customers/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify(customer.to_dict()), 200


@sales_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    
    customer = Customer(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        address=data.get('address')
    )
    
    db.session.add(customer)
    db.session.commit()
    
    return jsonify(customer.to_dict()), 201


@sales_bp.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)
    customer.is_active = data.get('is_active', customer.is_active)
    
    db.session.commit()
    
    return jsonify(customer.to_dict()), 200


@sales_bp.route('/sales-orders', methods=['GET'])
@jwt_required()
def get_sales_orders():
    orders = SalesOrder.query.all()
    return jsonify([o.to_dict() for o in orders]), 200


@sales_bp.route('/sales-orders/<int:id>', methods=['GET'])
@jwt_required()
def get_sales_order(id):
    order = SalesOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Sales order not found'}), 404
    return jsonify(order.to_dict()), 200


@sales_bp.route('/sales-orders', methods=['POST'])
@jwt_required()
def create_sales_order():
    data = request.get_json()
    
    order = SalesOrder(
        customer_id=data.get('customer_id'),
        order_number=generate_order_number(),
        expected_date=data.get('expected_date'),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(order)
    db.session.flush()
    
    total = 0
    for item_data in data.get('items', []):
        item = SalesOrderItem(
            sales_order_id=order.id,
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


@sales_bp.route('/sales-orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_sales_order(id):
    order = SalesOrder.query.get(id)
    if not order:
        return jsonify({'error': 'Sales order not found'}), 404
    
    data = request.get_json()
    order.status = data.get('status', order.status)
    order.notes = data.get('notes', order.notes)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 200


@sales_bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([i.to_dict() for i in invoices]), 200


@sales_bp.route('/invoices/<int:id>', methods=['GET'])
@jwt_required()
def get_invoice(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    return jsonify(invoice.to_dict()), 200


@sales_bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    data = request.get_json()
    
    invoice = Invoice(
        sales_order_id=data.get('sales_order_id'),
        invoice_number=generate_invoice_number(),
        due_date=data.get('due_date'),
        amount=data.get('amount', 0),
        notes=data.get('notes'),
        status='pending'
    )
    
    db.session.add(invoice)
    db.session.commit()
    
    return jsonify(invoice.to_dict()), 201


@sales_bp.route('/invoices/<int:id>', methods=['PUT'])
@jwt_required()
def update_invoice(id):
    invoice = Invoice.query.get(id)
    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404
    
    data = request.get_json()
    invoice.status = data.get('status', invoice.status)
    invoice.notes = data.get('notes', invoice.notes)
    
    db.session.commit()
    
    return jsonify(invoice.to_dict()), 200
