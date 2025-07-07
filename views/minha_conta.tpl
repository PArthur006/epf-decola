<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }} - Decola-Brasil</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>
<body>
    %include('barra_navegacao.tpl')

    <div class="container">
        <h1>Minha Conta</h1>
        
        <div class="caixa-perfil">
            <h3>Seus Dados</h3>
            <p><strong>Nome:</strong> {{usuario.name}}</p>
            <p><strong>Email:</strong> {{usuario.email}}</p>
        </div>

        <div class="historico-reservas">
            <h2>Suas Reservas</h2>
            
            % if not reservas:
                <p>Você ainda não fez nenhuma reserva.</p>
            % else:
                % for reserva in reservas:
                <div class="cartao-reserva">
                    <div class="info-voo-reserva">
                        <h4>Voo {{reserva.voo.numero_voo}} para {{reserva.voo.destino.cidade}}</h4>
                        <p>Data: {{reserva.voo.data_partida.strftime('%d/%m/%Y')}}</p>
                    </div>
                    <div class="info-assento-reserva">
                        <span>Assento</span>
                        <p>{{reserva.assento}}</p>
                    </div>
                    <div class="info-status-reserva status-{{reserva.status.lower()}}">
                        <span>Status</span>
                        <p>{{reserva.status}}</p>
                    </div>
                </div>
                % end
            % end
        </div>
    </div>
</body>
</html>