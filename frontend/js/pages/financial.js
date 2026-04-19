document.addEventListener('DOMContentLoaded', function() {
    if (!checkAuth()) return;
    loadAccounts();
    loadJournalEntries();
});

async function loadAccounts() {
    try {
        const accounts = await api.get('/financial/accounts');
        const tbody = document.querySelector('#accTable tbody');
        tbody.innerHTML = accounts.map(a => `
            <tr>
                <td>${a.code}</td>
                <td>${a.name}</td>
                <td>${a.account_type}</td>
                <td><span class="badge ${a.is_active ? 'bg-success' : 'bg-secondary'}">${a.is_active ? 'Active' : 'Inactive'}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="viewAccount(${a.id})">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load accounts:', error);
    }
}

async function loadJournalEntries() {
    try {
        const entries = await api.get('/financial/journal-entries');
        const tbody = document.querySelector('#jeTable tbody');
        tbody.innerHTML = entries.map(e => `
            <tr>
                <td>${e.entry_number}</td>
                <td>${e.entry_date || ''}</td>
                <td>${e.description || ''}</td>
                <td><span class="badge badge-${e.status}">${e.status}</span></td>
                <td><button class="btn btn-sm btn-info" onclick="viewJE(${e.id})">View</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load journal entries:', error);
    }
}

async function loadTrialBalance() {
    try {
        const tb = await api.get('/financial/trial-balance');
        const tbody = document.querySelector('#tbTable tbody');
        tbody.innerHTML = tb.accounts.map(a => `
            <tr>
                <td>${a.account_code}</td>
                <td>${a.account_name}</td>
                <td>$${a.debit.toFixed(2)}</td>
                <td>$${a.credit.toFixed(2)}</td>
            </tr>
        `).join('');
        tbody.innerHTML += `
            <tr class="table-info fw-bold">
                <td colspan="2">Totals</td>
                <td>$${tb.total_debit.toFixed(2)}</td>
                <td>$${tb.total_credit.toFixed(2)}</td>
            </tr>
        `;
    } catch (error) {
        console.error('Failed to load trial balance:', error);
    }
}
