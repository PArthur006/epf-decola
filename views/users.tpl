<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Decola - Brasil</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    %include("navbar.tpl")
    <header class="hero">
        <div class="hero-content">
            <img src="/static/img/hero.png" alt="Logo Decola-Brasil" class="hero-logo">
        </div>
    </header>

    <main class="packages-section">
        <h2>Pacotes e Destinos Populares</h2>

        <button id="prevBtn" class="nav-button prev-button">❮</button>

        <div class="packages-container" id="packagesContainer">
            
            
            <div class="card">
                <img src="/static/img/RioDeJaneiro.png" alt="destino1">
                <div class="card-content">
                    <h3>Rio de Janeiro</h3>
                    <p>A partir de R$ 450,00</p>
                </div>
            </div>
            <div class="card">
                <img src="/static/img/FernandoDeNoronha.png" alt="destino2">
                <div class="card-content">
                    <h3>Fernando de Noronha</h3>
                    <p>A partir de R$ 1.200,00</p>
                </div>
            </div>
            
            <div class="card">
                <img src="/static/img/Gramado.png" alt="destino3">
                <div class="card-content">
                    <h3>Gramado</h3>
                    <p>A partir de R$ 600,00</p>
                </div>
            </div>
            
            <div class="card">
                <img src="/static/img/SaoPaulo.png" alt="destino4">
                <div class="card-content">
                    <h3>São Paulo</h3>
                    <p>A partir de R$ 300,00</p>
                </div>
            </div>
            
            <div class="card">
                <img src="/static/img/Salvador.png" alt="destino5">
                <div class="card-content">
                    <h3>Salvador</h3>
                    <p>A partir de R$ 400,00</p>
                </div>
            </div>
        </div>

        <button id="nextBtn" class="nav-button next-button">❯</button>
    </main>
    <script src="/static/js/main.js"></script>
</body>
</html>