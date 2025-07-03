document.addEventListener('DOMContentLoaded', function() {

    // Pega os elementos do HTML
    const container = document.getElementById('packagesContainer');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (container && prevBtn && nextBtn) {
        
        const scrollAmount = container.querySelector('.card').offsetWidth + 20;
        
        // Define o comportamento dos botões de navegação
        nextBtn.addEventListener('click', function() {
            container.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        });

        prevBtn.addEventListener('click', function() {
            container.scrollBy({
                left: -scrollAmount,
                behavior: 'smooth'
            });
        });
    }

    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('passwordInput');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.textContent = type === 'password' ? '👁️' : '🙈';
        });
    }
});