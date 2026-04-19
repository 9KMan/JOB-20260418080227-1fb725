import pytest

def test_create_customer(client, auth_headers):
    response = client.post('/api/sales/customers',
        headers=auth_headers,
        json={
            'name': 'Test Customer',
            'email': 'customer@test.com',
            'phone': '9876543210',
            'address': '456 Customer Ave'
        })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Customer'

def test_create_sales_order(client, auth_headers):
    customer_response = client.post('/api/sales/customers',
        headers=auth_headers,
        json={
            'name': 'SO Customer',
            'email': 'socustomer@test.com',
            'phone': '9876543210',
            'address': '456 Customer Ave'
        })
    customer_id = customer_response.get_json()['id']
    
    response = client.post('/api/sales/sales-orders',
        headers=auth_headers,
        json={
            'customer_id': customer_id,
            'items': [
                {'product_name': 'Product A', 'quantity': 5, 'unit_price': 50.00}
            ]
        })
    assert response.status_code == 201
