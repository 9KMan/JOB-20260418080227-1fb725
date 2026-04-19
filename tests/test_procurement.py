import pytest

def test_create_supplier(client, auth_headers):
    response = client.post('/api/procurement/suppliers', 
        headers=auth_headers,
        json={
            'name': 'Test Supplier',
            'email': 'supplier@test.com',
            'phone': '1234567890',
            'address': '123 Test St'
        })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test Supplier'

def test_get_suppliers(client, auth_headers):
    response = client.get('/api/procurement/suppliers', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_purchase_order(client, auth_headers):
    supplier_response = client.post('/api/procurement/suppliers',
        headers=auth_headers,
        json={
            'name': 'PO Supplier',
            'email': 'posupplier@test.com',
            'phone': '1234567890',
            'address': '123 Test St'
        })
    supplier_id = supplier_response.get_json()['id']
    
    response = client.post('/api/procurement/purchase-orders',
        headers=auth_headers,
        json={
            'supplier_id': supplier_id,
            'items': [
                {'product_name': 'Widget', 'quantity': 100, 'unit_price': 10.00}
            ]
        })
    assert response.status_code == 201
