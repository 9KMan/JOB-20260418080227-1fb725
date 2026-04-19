document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegister = document.getElementById('showRegister');
    const registerCard = document.getElementById('registerCard');

    showRegister.addEventListener('click', function(e) {
        e.preventDefault();
        registerCard.style.display = registerCard.style.display === 'none' ? 'block' : 'none';
    });

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const data = await api.post('/auth/login', { username, password });
            api.setToken(data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            window.location.href = 'index.html';
        } catch (error) {
            alert('Login failed: ' + error.message);
        }
    });

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        try {
            await api.post('/auth/register', { username, email, password });
            alert('Registration successful! Please login.');
            registerCard.style.display = 'none';
            document.getElementById('username').value = username;
        } catch (error) {
            alert('Registration failed: ' + error.message);
        }
    });

    document.getElementById('logoutBtn')?.addEventListener('click', function(e) {
        e.preventDefault();
        api.clearToken();
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    });
});

function checkAuth() {
    if (!api.isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}
