<nav class="barra-navegacao">
    <div class="container-barra-navegacao">
        <a href="/" class="logo-barra-navegacao">Decola-BR</a>
        <ul class="menu-nav">

            % if usuario_logado:
                <li class="item-nav">
                    <a href="/voos" class="link-nav">Visualizar Voos</a>
                </li>
                <li class="item-nav">
                    <a href="/minha-conta" class="link-nav">Minha Conta</a>
                </li>
                <li class="item-nav">
                    <a href="/logout" class="link-nav btn-cadastro">Logout</a>
                </li>
            % else:
                <li class="item-nav">
                    <a href="/login" class="link-nav">Login</a>
                </li>
                <li class="item-nav">
                    <a href="/cadastro" class="link-nav btn-cadastro">Registrar</a>
                </li>
            % end

        </ul>
    </div>
</nav>
