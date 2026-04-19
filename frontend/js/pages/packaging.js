document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadPackagingOrders();
});

async function loadPackagingOrders() {
    try {
        const orders = await api.get('/packaging/packaging-orders');
        const tbody = document.querySelector('#pkgTable tbody');
        tbody.innerHTML = orders.map(o => `
            <tr>
                <td>${o.order_number}</td>
                <td>${o.sales_order_id || ''}</td>
                <td>${o.packaging_date || ''}</td>
                <td>${o.packed_by || ''}</td>
                <td><span class="badge badge-${o.status}">${o.status}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="viewPkg(${o.id})">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load packaging orders:', error);
    }
}
