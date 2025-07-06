<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
    <title>Cadastro - Decola-Brasil</title>
</head>
<body>
    %include("barra_navegacao.tpl") 

    <div class="container-pagina-formulario">
        <div class="caixa-formulario">
            <h2>Crie sua conta</h2>
            <form action="/cadastro" method="post">
                <div class="grupo-formulario">
                    <label for="nome">Nome Completo</label>
                    <input type="text" id="nome" name="nome" required>
                </div>
                <div class="grupo-formulario">
                    <label for="email">E-mail</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="grupo-formulario">
                    <label for="senhaCadastro">Senha</label>
                    <div class="wrapper-senha">
                        <input type="password" id="senhaCadastro" name="password" required>
                        <span id="toggleSenhaCadastro" class="toggle-senha">👁️</span>
                    </div>
                </div>
                <div class="grupo-formulario">
                    <label for="confirmarSenha">Confirme sua Senha</label>
                    <div class="wrapper-senha">
                        <input type="password" id="confirmarSenha" name="confirm_password" required>
                        <span id="toggleConfirmarSenha" class="toggle-senha">👁️</span>
                    </div>
                </div>
                <button type="submit" class="btn-largura-total">Criar conta</button>
            </form>
            <div class="rodape-formulario">
                <p>Já tem uma conta? <a href="/login">Faça login</a></p>
            </div>
        </div>
    </div>
    <script src="/static/js/main.js"></script>
</body>
</html>