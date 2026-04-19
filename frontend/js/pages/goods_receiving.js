document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadGRNs();
});

async function loadGRNs() {
    try {
        const grns = await api.get('/goods-receiving/grn');
        const tbody = document.querySelector('#grnTable tbody');
        tbody.innerHTML = grns.map(g => `
            <tr>
                <td>${g.grn_number}</td>
                <td>${g.purchase_order_id || ''}</td>
                <td>${g.received_date || ''}</td>
                <td>${g.received_by || ''}</td>
                <td><span class="badge badge-${g.status}">${g.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="viewGRN(${g.id})">View</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load GRNs:', error);
    }
}
