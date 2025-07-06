<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
    <title>{{titulo}} - Decola-Brasil</title>
</head>
<body>
    %include('barra_navegacao.tpl')

    <div class="container">
        <h1>{{titulo}}</h1>

        <div class="grade-voos">
            % for voo in voos:
            <div class="cartao-voo-interativo" data-voo-id="{{voo.numero_voo}}">
                
                <img src="{{voo.destino.imagem}}" alt="Foto do destino {{voo.destino.cidade}}">
                
                <div class="secao-cartao info-basica">
                    <h3>{{voo.destino.cidade}}</h3>
                    <p>A partir de R$ {{voo.preco}}</p>
                </div>

                <div class="secao-cartao info-hover">
                    <p>Assentos disponíveis: {{voo.assentos_disp}}</p>
                </div>

                <div class="secao-cartao info-expandida">
                    <p><strong>Companhia:</strong> {{voo.comp_aerea}}</p>
                    <p><strong>Embarque:</strong> {{voo.data_partida.strftime('%H:%M')}}</p>
                    <a href="/assentos/{{voo.numero_voo}}" class="btn-largura-total">Escolher Assentos</a>
                </div>
            </div>
            % end
        </div>
    </div>
    <script src="/static/js/main.js"></script>
</body>
</html>