<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="../static/css/style.css">
    <title>Cadastro - Decola-Brasil</title>
</head>
<body>
    <div class="form-page-container">
        <div class="form-box">
            <h2>Crie sua conta</h2>
            <form action="/signup" method="post">
                <div class="form-group">
                    <label for="name">Nome Completo</label>
                    <input type="text" id="name" name="name" required>
                </div>
                <div class="form-group">
                    <label for="email">E-mail</label>
                    <input type="email" id="email" name="email" required>
                </div>
                <div class="form-group">
                    <label for="password">Senha</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="confirm_password">Confirme sua Senha</label>
                    <input type="password" id="confirm_password" name="confirm_password" required>
                </div>
                <button type="submit" class="btn-full">Criar conta</button>
            </form>
            <div class="form-footer">
                <p>Já tem uma conta? <a href="/login">Faça login</a></p>
            </div>
        </div>
    </div>
</body>
</html>