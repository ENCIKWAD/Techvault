document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const result = await APIClient.post('/auth/login', { email, password });

            if (result && result.id) {
                localStorage.setItem('userId', result.id);
                localStorage.setItem('userRole', result.role);
                localStorage.setItem('username', result.username);
                document.getElementById('login-message').textContent = 'Login successful!';
                setTimeout(() => window.location.href = 'index.html', 1000);
            } else {
                document.getElementById('login-message').textContent = 'Login failed!';
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const result = await APIClient.post('/auth/register', { username, email, password });

            if (result && result.success) {
                document.getElementById('register-message').textContent = 'Registration successful! Redirecting...';
                setTimeout(() => window.location.href = 'login.html', 1000);
            } else {
                document.getElementById('register-message').textContent = 'Registration failed!';
            }
        });
    }
});
