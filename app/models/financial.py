from datetime import datetime
from app.extensions import db


class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    children = db.relationship('Account', backref=db.backref('parent', remote_side=[id]))
    journal_lines = db.relationship('JournalLineItem', back_populates='account')

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'account_type': self.account_type,
            'parent_id': self.parent_id,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    entry_number = db.Column(db.String(50), unique=True, nullable=False)
    entry_date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text)
    reference = db.Column(db.String(100))
    status = db.Column(db.String(50), default='draft')
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    lines = db.relationship('JournalLineItem', back_populates='journal_entry', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'entry_number': self.entry_number,
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'description': self.description,
            'reference': self.reference,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'lines': [line.to_dict() for line in self.lines]
        }


class JournalLineItem(db.Model):
    __tablename__ = 'journal_line_items'

    id = db.Column(db.Integer, primary_key=True)
    journal_entry_id = db.Column(db.Integer, db.ForeignKey('journal_entries.id'), nullable=False)
    account_code = db.Column(db.String(50), db.ForeignKey('accounts.code'), nullable=False)
    debit = db.Column(db.Numeric(12, 2), default=0)
    credit = db.Column(db.Numeric(12, 2), default=0)
    description = db.Column(db.Text)

    journal_entry = db.relationship('JournalEntry', back_populates='lines')
    account = db.relationship('Account', back_populates='journal_lines')

    def to_dict(self):
        return {
            'id': self.id,
            'journal_entry_id': self.journal_entry_id,
            'account_code': self.account_code,
            'debit': float(self.debit) if self.debit else 0,
            'credit': float(self.credit) if self.credit else 0,
            'description': self.description
        }


class TrialBalance(db.Model):
    __tablename__ = 'trial_balances'

    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, nullable=False)
    account_code = db.Column(db.String(50), db.ForeignKey('accounts.code'), nullable=False)
    account_name = db.Column(db.String(255))
    debit = db.Column(db.Numeric(12, 2), default=0)
    credit = db.Column(db.Numeric(12, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'report_date': self.report_date.isoformat() if self.report_date else None,
            'account_code': self.account_code,
            'account_name': self.account_name,
            'debit': float(self.debit) if self.debit else 0,
            'credit': float(self.credit) if self.credit else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
