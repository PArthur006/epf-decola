<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="../static/css/style.css">
    <title>Cadastro - Decola-Brasil</title>
</head>
<body>
    %include("navbar.tpl") 

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
                    <div class="password-wrapper">
                        <input type="password" id="signupPassword" name="password" required>
                        <span id="toggleSignupPassword" class="toggle-password">👁️</span>
                    </div>
                </div>
                <div class="form-group">
                    <label for="confirmPassword">Confirme sua Senha</label>
                    <div class="password-wrapper">
                        <input type="password" id="confirmPassword" name="confirm_password" required>
                        <span id="toggleConfirmPassword" class="toggle-password">👁️</span>
                    </div>
                </div>
                <button type="submit" class="btn-full">Criar conta</button>
            </form>
            <div class="form-footer">
                <p>Já tem uma conta? <a href="/login">Faça login</a></p>
            </div>
        </div>
    </div>

    <script src="static/js/main.js"></script>
</body>
</html>