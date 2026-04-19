document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadCustomers();
    loadSalesOrders();
    loadInvoices();
});

async function loadCustomers() {
    try {
        const customers = await api.get('/sales/customers');
        const tbody = document.querySelector('#custTable tbody');
        tbody.innerHTML = customers.map(c => `
            <tr>
                <td>${c.name}</td>
                <td>${c.email || ''}</td>
                <td>${c.phone || ''}</td>
                <td><span class="badge ${c.is_active ? 'bg-success' : 'bg-secondary'}">${c.is_active ? 'Active' : 'Inactive'}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="editCustomer(${c.id})">Edit</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load customers:', error);
    }
}

async function loadSalesOrders() {
    try {
        const orders = await api.get('/sales/sales-orders');
        const tbody = document.querySelector('#soTable tbody');
        tbody.innerHTML = orders.map(o => `
            <tr>
                <td>${o.order_number}</td>
                <td>${o.customer_id || ''}</td>
                <td>${o.order_date || ''}</td>
                <td>$${o.total_amount.toFixed(2)}</td>
                <td><span class="badge badge-${o.status}">${o.status}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="viewSO(${o.id})">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load sales orders:', error);
    }
}

async function loadInvoices() {
    try {
        const invoices = await api.get('/sales/invoices');
        const tbody = document.querySelector('#invTable tbody');
        tbody.innerHTML = invoices.map(i => `
            <tr>
                <td>${i.invoice_number}</td>
                <td>${i.sales_order_id || ''}</td>
                <td>${i.invoice_date || ''}</td>
                <td>$${i.amount.toFixed(2)}</td>
                <td><span class="badge badge-${i.status}">${i.status}</span></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load invoices:', error);
    }
}
