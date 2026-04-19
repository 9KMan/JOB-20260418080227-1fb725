document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadDashboardData();
});

async function loadDashboardData() {
    try {
        const [pos, grns, wos, sos] = await Promise.all([
            api.get('/procurement/purchase-orders'),
            api.get('/goods-receiving/grn'),
            api.get('/production/work-orders'),
            api.get('/sales/sales-orders')
        ]);

        document.getElementById('poCount').textContent = pos.length;
        document.getElementById('grnCount').textContent = grns.length;
        document.getElementById('woCount').textContent = wos.length;
        document.getElementById('soCount').textContent = sos.length;

        const recentActivity = document.getElementById('recentActivity');
        recentActivity.innerHTML = '';

        const recentItems = [
            ...pos.slice(-3).map(p => ({ type: 'PO', data: p, date: p.created_at })),
            ...sos.slice(-3).map(s => ({ type: 'SO', data: s, date: s.created_at })),
            ...wos.slice(-3).map(w => ({ type: 'WO', data: w, date: w.created_at }))
        ].sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 5);

        if (recentItems.length === 0) {
            recentActivity.innerHTML = '<li class="list-group-item">No recent activity</li>';
        } else {
            recentItems.forEach(item => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = `${item.type}: ${item.data.order_number || item.data.order_number || item.data.order_number} - ${item.data.status}`;
                recentActivity.appendChild(li);
            });
        }
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}
