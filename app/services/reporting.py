from datetime import datetime

def generate_inventory_report():
    return {
        'report_name': 'Inventory Report',
        'generated_at': datetime.now().isoformat(),
        'items': []
    }

def generate_sales_report():
    return {
        'report_name': 'Sales Report',
        'generated_at': datetime.now().isoformat(),
        'total_sales': 0,
        'orders': []
    }

def generate_financial_summary():
    return {
        'report_name': 'Financial Summary',
        'generated_at': datetime.now().isoformat(),
        'total_revenue': 0,
        'total_expenses': 0,
        'net_income': 0
    }

def generate_production_report():
    return {
        'report_name': 'Production Report',
        'generated_at': datetime.now().isoformat(),
        'work_orders': [],
        'output_summary': {}
    }
