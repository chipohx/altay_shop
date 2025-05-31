document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    updateAuthUI(token);

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                username: formData.get('username'),
                password: formData.get('password')
            };
            
            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams(data)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    // Store the token
                    localStorage.setItem('token', result.access_token);
                    // Update UI
                    updateAuthUI(result.access_token);
                    // Redirect to main service
                    window.location.href = 'http://localhost:8004/';
                } else {
                    const error = await response.json();
                    alert(error.detail || 'Ошибка входа');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Произошла ошибка при входе');
            }
        });
    }
    
    // Registration form handling
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                alert('Пароли не совпадают');
                return;
            }
            
            const formData = new FormData(this);
            const data = {
                email: formData.get('email'),
                username: formData.get('username'),
                password: formData.get('password')
            };
            
            try {
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    alert('Регистрация успешна! Теперь вы можете войти.');
                    window.location.href = '/auth/login';
                } else {
                    const error = await response.json();
                    alert(error.detail || 'Ошибка регистрации');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Произошла ошибка при регистрации');
            }
        });
    }

    // Logout handling
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('token');
            updateAuthUI(null);
            window.location.href = '/auth/login';
        });
    }
});

function updateAuthUI(token) {
    const authLinks = document.querySelector('.auth-links');
    const userLinks = document.querySelector('.user-links');
    
    if (token) {
        if (authLinks) authLinks.style.display = 'none';
        if (userLinks) userLinks.style.display = 'flex';
    } else {
        if (authLinks) authLinks.style.display = 'flex';
        if (userLinks) userLinks.style.display = 'none';
    }
} 