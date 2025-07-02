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
});