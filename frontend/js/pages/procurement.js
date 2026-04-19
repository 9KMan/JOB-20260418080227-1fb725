document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadSuppliers();
    loadPurchaseOrders();
    loadRequisitions();
});

async function loadSuppliers() {
    try {
        const suppliers = await api.get('/procurement/suppliers');
        const tbody = document.querySelector('#suppliersTable tbody');
        tbody.innerHTML = suppliers.map(s => `
            <tr>
                <td>${s.name}</td>
                <td>${s.email || ''}</td>
                <td>${s.phone || ''}</td>
                <td><span class="badge ${s.is_active ? 'bg-success' : 'bg-secondary'}">${s.is_active ? 'Active' : 'Inactive'}</span></td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="editSupplier(${s.id})">Edit</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load suppliers:', error);
    }
}

async function loadPurchaseOrders() {
    try {
        const orders = await api.get('/procurement/purchase-orders');
        const tbody = document.querySelector('#poTable tbody');
        tbody.innerHTML = orders.map(o => `
            <tr>
                <td>${o.order_number}</td>
                <td>${o.supplier_id || ''}</td>
                <td>${o.order_date || ''}</td>
                <td>$${o.total_amount.toFixed(2)}</td>
                <td><span class="badge badge-${o.status}">${o.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="viewPO(${o.id})">View</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load purchase orders:', error);
    }
}

async function loadRequisitions() {
    try {
        const requisitions = await api.get('/procurement/purchase-requisitions');
        const tbody = document.querySelector('#prTable tbody');
        tbody.innerHTML = requisitions.map(r => `
            <tr>
                <td>${r.request_number}</td>
                <td>${r.department || ''}</td>
                <td>${r.requested_by || ''}</td>
                <td>${r.request_date || ''}</td>
                <td><span class="badge badge-${r.status}">${r.status}</span></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load requisitions:', error);
    }
}
