<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }}</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>
<body>
    %include('barra_navegacao.tpl')

    <div class="container-aviao">
        <h1>Escolha seu Assento</h1>
        <div class="aviao">
            <div class="secao-aviao bico-aviao">BICO</div>
            
            <div class="mapa-assentos">
                % for fileira in range(1, aviao['fileiras'] + 1):
                    % for letra_assento in aviao['layout']:
                        % if letra_assento is None:
                            <div class="corredor">{{fileira}}</div>
                        % else:
                            % id_assento = f"{letra_assento}{fileira}"
                            % status = 'ocupado' if id_assento in aviao['assentos_ocupados'] else 'disponivel'
                            <div class="assento {{status}}" data-assento="{{id_assento}}">{{id_assento}}</div>
                        % end
                    % end

                    % if fileira == 10:
                        <div class="marcador-saida">Porta de Emergência</div>
                    % end
                    
                    % if fileira == 12:
                        <div class="secao-aviao asas-aviao">ASAS</div>
                    % end
                % end
            </div>
            
            <div class="secao-aviao cauda-aviao">CAUDA</div>
        </div>

        <div class="resumo-reserva">
            <div class="info-assentos-selecionados">
                <span>Assentos escolhidos:</span>
                <span id="listaAssentosSelecionados">Nenhum</span>
            </div>
            <button class="btn-largura-total" id="botaoPagar">Pagar</button>
        </div>
    </div>
    <script src="/static/js/main.js"></script>
</body>
</html>