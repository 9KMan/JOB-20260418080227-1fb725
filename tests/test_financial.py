import pytest

def test_create_account(client, auth_headers):
    response = client.post('/api/financial/accounts',
        headers=auth_headers,
        json={
            'code': '1000',
            'name': 'Cash',
            'account_type': 'asset'
        })
    assert response.status_code == 201
    data = response.get_json()
    assert data['code'] == '1000'

def test_create_journal_entry(client, auth_headers):
    client.post('/api/financial/accounts',
        headers=auth_headers,
        json={'code': '1000', 'name': 'Cash', 'account_type': 'asset'})
    client.post('/api/financial/accounts',
        headers=auth_headers,
        json={'code': '4000', 'name': 'Sales Revenue', 'account_type': 'revenue'})
    
    response = client.post('/api/financial/journal-entries',
        headers=auth_headers,
        json={
            'description': 'Sale transaction',
            'lines': [
                {'account_code': '1000', 'debit': 500.00, 'credit': 0},
                {'account_code': '4000', 'debit': 0, 'credit': 500.00}
            ]
        })
    assert response.status_code == 201
