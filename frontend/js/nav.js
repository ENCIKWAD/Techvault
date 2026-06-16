document.addEventListener('DOMContentLoaded', () => {
    const userId   = localStorage.getItem('userId');
    const userRole = localStorage.getItem('userRole');
    const username = localStorage.getItem('username');
    const navLinks = document.getElementById('nav-links');

    if (!navLinks) return;

    if (userId) {
        const isAdmin = userRole === 'admin';
        navLinks.innerHTML = `
            ${isAdmin ? '<li><a href="admin.html">Dashboard</a></li>' : '<li><a href="cart.html">Cart</a></li>'}
            <li><a href="orders.html">${isAdmin ? 'Orders' : 'My Orders'}</a></li>
            <li class="nav-profile">
                <div class="profile-indicator">
                    <span class="profile-name">&#128100; ${username || 'User'}</span>
                    <span class="role-badge ${isAdmin ? 'badge-admin' : 'badge-customer'}">
                        ${isAdmin ? 'Admin' : 'Customer'}
                    </span>
                </div>
                <button onclick="logout()" class="btn-logout">Logout</button>
            </li>
        `;
    } else {
        navLinks.innerHTML = `
            <li><a href="login.html">Login</a></li>
        `;
    }
});

function logout() {
    localStorage.removeItem('userId');
    localStorage.removeItem('userRole');
    localStorage.removeItem('username');
    window.location.href = 'index.html';
}
