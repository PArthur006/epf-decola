<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Decola-Brasil</title>
    <link rel="stylesheet" type="text/css" href="static/css/style.css">
</head>
<body>
    %include("navbar.tpl")
    <div class="form-page-container">
        <div class="form-box">
            <h2>Acesse sua conta</h2>
            <form action="/login" method="post">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>

                </div>
                <div class="form-group">
                    <label for="password">Senha</label>
                    <div class="password-wrapper">
                        <input type="password" name="password" id="passwordInput" required>
                        <span id="togglePassword" class="toggle-password">👁️</span>
                    </div>
                </div>
                <button type="submit" class="btn-full">Entrar</button>
            </form>
            <div class="form-footer">
                <p>Não tem uma conta? <a href="/signup">Cadastre-se</a></p>
            </div>
        </div>
    </div>

    <script src="static/js/main.js"></script>
</body>
</html>