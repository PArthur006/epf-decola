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

    // Função genérica para alternar a visibilidade de senha
    function togglePasswordVisibility(inputElement, toggleElement) {
        if (inputElement && toggleElement) {
            toggleElement.addEventListener('click', function() {
                const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
                inputElement.setAttribute('type', type)
                this.textContent = type === 'password' ? '👁️' : '🙈';
            })
        }
    }

    // Pega os elementos do campo de senha do login
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('passwordInput');

    togglePasswordVisibility(passwordInput, togglePassword);

    // Pega os elementos do primeiro campo de senha do cadastro
    const signupPassowordInput = document.getElementById('signupPassword');
    const toggleSignupPasswordBtn = document.getElementById('toggleSignupPassword');

    // Pega os elementos do segundo campo de senha do cadastro
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const toggleConfirmPasswordBtn = document.getElementById('toggleConfirmPassword');

    // Alterna a visibilidade da senha do cadastro
    togglePasswordVisibility(signupPassowordInput, toggleSignupPasswordBtn);
    togglePasswordVisibility(confirmPasswordInput, toggleConfirmPasswordBtn);
});