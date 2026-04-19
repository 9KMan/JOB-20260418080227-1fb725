from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.financial import Account, JournalEntry, JournalLineItem, TrialBalance
from datetime import datetime
import uuid

financial_bp = Blueprint('financial', __name__)

def generate_entry_number():
    return f"JE-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"


@financial_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    accounts = Account.query.all()
    return jsonify([a.to_dict() for a in accounts]), 200


@financial_bp.route('/accounts/<int:id>', methods=['GET'])
@jwt_required()
def get_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    return jsonify(account.to_dict()), 200


@financial_bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    data = request.get_json()
    
    account = Account(
        code=data.get('code'),
        name=data.get('name'),
        account_type=data.get('account_type'),
        parent_id=data.get('parent_id'),
        description=data.get('description')
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify(account.to_dict()), 201


@financial_bp.route('/accounts/<int:id>', methods=['PUT'])
@jwt_required()
def update_account(id):
    account = Account.query.get(id)
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    data = request.get_json()
    account.name = data.get('name', account.name)
    account.account_type = data.get('account_type', account.account_type)
    account.description = data.get('description', account.description)
    account.is_active = data.get('is_active', account.is_active)
    
    db.session.commit()
    
    return jsonify(account.to_dict()), 200


@financial_bp.route('/journal-entries', methods=['GET'])
@jwt_required()
def get_journal_entries():
    entries = JournalEntry.query.all()
    return jsonify([e.to_dict() for e in entries]), 200


@financial_bp.route('/journal-entries/<int:id>', methods=['GET'])
@jwt_required()
def get_journal_entry(id):
    entry = JournalEntry.query.get(id)
    if not entry:
        return jsonify({'error': 'Journal entry not found'}), 404
    return jsonify(entry.to_dict()), 200


@financial_bp.route('/journal-entries', methods=['POST'])
@jwt_required()
def create_journal_entry():
    data = request.get_json()
    
    entry = JournalEntry(
        entry_number=generate_entry_number(),
        description=data.get('description'),
        reference=data.get('reference'),
        status='draft'
    )
    
    db.session.add(entry)
    db.session.flush()
    
    for line_data in data.get('lines', []):
        line = JournalLineItem(
            journal_entry_id=entry.id,
            account_code=line_data.get('account_code'),
            debit=line_data.get('debit', 0),
            credit=line_data.get('credit', 0),
            description=line_data.get('description')
        )
        db.session.add(line)
    
    db.session.commit()
    
    return jsonify(entry.to_dict()), 201


@financial_bp.route('/journal-entries/<int:id>', methods=['PUT'])
@jwt_required()
def update_journal_entry(id):
    entry = JournalEntry.query.get(id)
    if not entry:
        return jsonify({'error': 'Journal entry not found'}), 404
    
    data = request.get_json()
    entry.status = data.get('status', entry.status)
    entry.description = data.get('description', entry.description)
    
    db.session.commit()
    
    return jsonify(entry.to_dict()), 200


@financial_bp.route('/trial-balance', methods=['GET'])
@jwt_required()
def get_trial_balance():
    accounts = Account.query.filter_by(is_active=True).all()
    
    trial_balance_data = []
    total_debit = 0
    total_credit = 0
    
    for account in accounts:
        debit = 0
        credit = 0
        
        for line in account.journal_lines:
            if line.journal_entry.status == 'posted':
                debit += float(line.debit or 0)
                credit += float(line.credit or 0)
        
        if account.account_type in ['asset', 'expense']:
            balance = debit - credit
            if balance >= 0:
                trial_balance_data.append({
                    'account_code': account.code,
                    'account_name': account.name,
                    'debit': balance,
                    'credit': 0
                })
                total_debit += balance
            else:
                trial_balance_data.append({
                    'account_code': account.code,
                    'account_name': account.name,
                    'debit': 0,
                    'credit': abs(balance)
                })
                total_credit += abs(balance)
        else:
            balance = credit - debit
            if balance >= 0:
                trial_balance_data.append({
                    'account_code': account.code,
                    'account_name': account.name,
                    'debit': 0,
                    'credit': balance
                })
                total_credit += balance
            else:
                trial_balance_data.append({
                    'account_code': account.code,
                    'account_name': account.name,
                    'debit': abs(balance),
                    'credit': 0
                })
                total_debit += abs(balance)
    
    return jsonify({
        'report_date': datetime.now().date().isoformat(),
        'accounts': trial_balance_data,
        'total_debit': total_debit,
        'total_credit': total_credit
    }), 200
