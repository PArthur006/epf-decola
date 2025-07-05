<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Decola-Brasil</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    %include("barra_navegacao.tpl")

    <header class="secao-hero">
        <div class="conteudo-hero">
            <img src="/static/img/hero.png" alt="Logo Decola-Brasil" class="logo-hero">
        </div>
    </header>

    <main class="secao-pacotes">
        <h2>Pacotes e Destinos Populares</h2>

        <button id="btnAnterior" class="botao-navegacao botao-anterior">❮</button>

        <div class="container-pacotes" id="containerPacotes">
            
            % for destino in destinos_populares:
            <div class="cartao">
                <img src="{{destino.imagem}}" alt="Foto do destino {{destino.cidade}}">
                <div class="conteudo-cartao">
                    <h3>{{destino.cidade}}</h3>
                    <p>A partir de R$ {{destino.preco}}</p>
                </div>
            </div>
            % end

        </div>

        <button id="btnProximo" class="botao-navegacao botao-proximo">❯</button>
    </main>
    
    <script src="/static/js/main.js"></script>
</body>
</html>