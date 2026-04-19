document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadBOMs();
    loadWorkOrders();
});

async function loadBOMs() {
    try {
        const boms = await api.get('/production/bom');
        const tbody = document.querySelector('#bomTable tbody');
        tbody.innerHTML = boms.map(b => `
            <tr>
                <td>${b.product_code}</td>
                <td>${b.product_name}</td>
                <td>${b.version || '1.0'}</td>
                <td><span class="badge ${b.is_active ? 'bg-success' : 'bg-secondary'}">${b.is_active ? 'Active' : 'Inactive'}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="viewBOM(${b.id})">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load BOMs:', error);
    }
}

async function loadWorkOrders() {
    try {
        const orders = await api.get('/production/work-orders');
        const tbody = document.querySelector('#woTable tbody');
        tbody.innerHTML = orders.map(o => `
            <tr>
                <td>${o.order_number}</td>
                <td>${o.product_name}</td>
                <td>${o.quantity_to_produce}</td>
                <td>${o.scheduled_start_date || ''} - ${o.scheduled_end_date || ''}</td>
                <td><span class="badge badge-${o.status}">${o.status}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="viewWO(${o.id})">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load work orders:', error);
    }
}
