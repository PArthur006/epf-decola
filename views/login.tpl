<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Decola-Brasil</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
</head>
<body>
    %include("barra_navegacao.tpl")

    <div class="container-pagina-formulario">
        <div class="caixa-formulario">
            <h2>Acesse sua conta</h2>
            <form action="/login" method="post">
                <div class="grupo-formulario">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="grupo-formulario">
                    <label for="senha">Senha</label>
                    <div class="wrapper-senha">
                        <input type="password" name="password" id="senha" required>
                        <span id="toggleSenha" class="toggle-senha">👁️</span>
                    </div>
                </div>
                <button type="submit" class="btn-largura-total">Entrar</button>
            </form>
            <div class="rodape-formulario">
                <p>Não tem uma conta? <a href="/cadastro">Cadastre-se</a></p>
            </div>
        </div>
    </div>
    <script src="/static/js/main.js"></script>
</body>
</html>