<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="../static/css/style.css">
    <title>{{title}} - Decola-Brasil</title>
</head>
<body>
    %include('navbar.tpl')

    <div class="container">
        <h1>{{title}}</h1>

        <div class="flight-grid">
            % for flight in flights:
            <div class="flight-card-interactive" data-flight-id="{{flight['id']}}">
                <img src="{{flight['imagem']}}" alt="Foto do destino {{flight['destino']}}">
                
                <div class="card-section basic-info">
                    <h3>{{flight['destino']}}</h3>
                    <p>A partir de R$ {{flight['preco']}}</p>
                </div>

                <div class="card-section hover-info">
                    <p>Poltronas disponíveis: {{flight['poltronas_disp']}}</p>
                </div>

                <div class="card-section expanded-info">
                    <p><strong>Companhia:</strong> {{flight['companhia']}}</p>
                    <p><strong>Embarque:</strong> {{flight['embarque']}}</p>
                    <p><strong>Piloto:</strong> {{flight['piloto']}}</p>
                    <a href="/seats/{{flight['id']}}" class="btn-full">Escolher Assentos</a>
                </div>
            </div>
            % end
        </div>
    </div>
    <script src="static/js/main.js"></script>
</body>
</html>