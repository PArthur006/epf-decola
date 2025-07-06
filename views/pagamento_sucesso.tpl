<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>{{titulo}} - Decola-Brasil</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <style>
      .mensagem-sucesso {
        margin-bottom: 20px;
      }
    </style>
</head>
<body>
    %include('barra_navegacao.tpl')

    <div class="container">
        <h1>{{titulo}}</h1>
        <p class="mensagem-sucesso"> Pagamento de <strong>R$ {{valor}}</strong> efetuado com sucesso!</p>

        <a href="/voos" class="btn btn-largura-total"> Voltar para voos disponíveis</a>
    </div>
</body>
</html>


