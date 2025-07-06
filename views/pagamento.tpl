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
        <h1>Confirmação e Pagamento</h1>
        <div class="layout-pagamento">

            <div class="resumo-compra">
                <h3>Resumo da sua Viagem</h3>
                <div class="item-resumo">
                    <span>Voo</span>
                    <p>{{reserva.voo.destino.cidade}}</p>
                </div>
                <div class="item-resumo">
                    <span>Data</span>
                    <p>{{reserva.voo.data_partida.strftime('%d/%m/%Y')}} às {{reserva.voo.data_partida.strftime('%H:%M')}}</p>
                </div>
                <div class="item-resumo">
                    <span>Assentos</span>
                    <p><b>{{ ', '.join(reserva.assentos) }}</b></p>
                </div>
                <hr>
                <div class="item-resumo total-compra">
                    <span>Total</span>
                    <p>R$ {{ '%.2f' % reserva.custo['total'] }}</p> </div>
            </div>

            <div class="formulario-pagamento">
                <h3>Dados do Cartão de Crédito</h3>
                <form action="/pagamento/{{reserva.voo.numero_voo}}/{{','.join(reserva.assentos)}}" method="post">
                    <div class="grupo-formulario">
                        <label for="nomeCartao">Nome no Cartão</label>
                        <input type="text" id="nomeCartao" name="nomeCartao" required>
                    </div>
                    <div class="grupo-formulario">
                        <label for="numeroCartao">Número do Cartão</label>
                        <input type="text" id="numeroCartao" name="numeroCartao" required>
                    </div>
                    <div class="grupo-formulario-duplo">
                        <div class="grupo-formulario">
                            <label for="validade">Validade (MM/AA)</label>
                            <input type="text" id="validade" name="validade" placeholder="MM/AA" required>
                        </div>
                        <div class="grupo-formulario">
                            <label for="cvv">CVV</label>
                            <input type="text" id="cvv" name="cvv" required>
                        </div>
                    </div>
                    <button type="submit" class="btn-largura-total">Confirmar Pagamento</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>