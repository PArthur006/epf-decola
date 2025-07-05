document.addEventListener('DOMContentLoaded', function() {

    // ==========================================================================
    // SEÇÃO 1: LÓGICA DO CARROSSEL DE PACOTES (Página Inicial)
    // ==========================================================================
    const containerPacotes = document.getElementById('containerPacotes');
    
    // Este 'if' garante que o código do carrossel só rode se os elementos existirem na página atual.
    if (containerPacotes) {
        const btnAnterior = document.getElementById('btnAnterior');
        const btnProximo = document.getElementById('btnProximo');
        
        // Verifica se todos os componentes do carrossel estão presentes.
        if (btnAnterior && btnProximo) {
            // Calcula o tamanho do deslocamento (largura de um card + o espaço entre eles).
            const tamanhoScroll = containerPacotes.querySelector('.cartao').offsetWidth + 20;

            // Adiciona o evento de clique para o botão "Próximo".
            btnProximo.addEventListener('click', () => {
                containerPacotes.scrollBy({
                    left: tamanhoScroll,
                    behavior: 'smooth' // Animação de rolagem suave.
                });
            });

            // Adiciona o evento de clique para o botão "Anterior".
            btnAnterior.addEventListener('click', () => {
                containerPacotes.scrollBy({
                    left: -tamanhoScroll, // O valor negativo rola para a esquerda.
                    behavior: 'smooth'
                });
            });
        }
    }

    // ==========================================================================
    // SEÇÃO 2: LÓGICA DE MOSTRAR/OCULTAR SENHA (Páginas de Login e Cadastro)
    // ==========================================================================

    // Função genérica e reutilizável para alternar a visibilidade de qualquer campo de senha.
    function configurarToggleSenha(idCampo, idToggle) {
        const campoSenha = document.getElementById(idCampo);
        const botaoToggle = document.getElementById(idToggle);

        if (campoSenha && botaoToggle) {
            botaoToggle.addEventListener('click', function() {
                // Verifica o tipo atual do campo e alterna entre 'password' e 'text'.
                const tipo = campoSenha.getAttribute('type') === 'password' ? 'text' : 'password';
                campoSenha.setAttribute('type', tipo);
                // Alterna o ícone de olho.
                this.textContent = tipo === 'password' ? '👁️' : '🙈';
            });
        }
    }

    // Aplica a função para os campos específicos de cada página.
    configurarToggleSenha('senha', 'toggleSenha'); // Página de Login
    configurarToggleSenha('senhaCadastro', 'toggleSenhaCadastro'); // Página de Cadastro
    configurarToggleSenha('confirmarSenha', 'toggleConfirmarSenha'); // Página de Cadastro


    // ==========================================================================
    // SEÇÃO 3: LÓGICA DE EXPANDIR CARD DE VOO (Página de Lista de Voos)
    // ==========================================================================
    const cartoesVoo = document.querySelectorAll('.cartao-voo-interativo');

    // Garante que o código só rode se houver cards de voo na página.
    if (cartoesVoo.length > 0) {
        cartoesVoo.forEach(cartao => {
            cartao.addEventListener('click', () => {
                // Adiciona ou remove a classe 'esta-expandido' no card clicado.
                // O CSS cuida de fazer a animação de expandir/recolher.
                cartao.classList.toggle('esta-expandido');
            });
        });
    }

    // ==========================================================================
    // SEÇÃO 4: LÓGICA DA PÁGINA DE SELEÇÃO DE ASSENTOS
    // ==========================================================================
    const mapaAssentos = document.querySelector('.mapa-assentos');

    if (mapaAssentos) {
        const listaAssentosEl = document.getElementById('listaAssentosSelecionados');
        const botaoPagarEl = document.getElementById('botaoPagar');
        
        mapaAssentos.addEventListener('click', function(event) {
            const elementoClicado = event.target;

            if (elementoClicado.classList.contains('assento') && elementoClicado.classList.contains('disponivel')) {
                elementoClicado.classList.toggle('selecionado');
                atualizarResumoAssentos();
            }
        });

        botaoPagarEl.addEventListener('click', function() {
            // Pega a lista de nomes dos assentos
            const assentosSelecionados = document.querySelectorAll('.assento.selecionado');
            const nomesDosAssentos = Array.from(assentosSelecionados).map(assento => assento.dataset.assento);
            
            if (nomesDosAssentos.length === 0) {
                alert('Por favor, selecione pelo menos um assento.');
                return; // Para a execução se nenhum assento foi selecionado
            }

            // Pega o ID do voo da URL atual (ex: /assentos/DB101)
            const urlPath = window.location.pathname.split('/');
            const idVoo = urlPath[urlPath.length - 1];
            
            // Constrói a URL final e redireciona o usuário
            const urlDestino = `/pagamento/${idVoo}/${nomesDosAssentos.join(',')}`;
            console.log("Redirecionando para:", urlDestino); // Para debug
            window.location.href = urlDestino;
        });

        function atualizarResumoAssentos() {
            const assentosSelecionados = document.querySelectorAll('.assento.selecionado');
            const nomesDosAssentos = Array.from(assentosSelecionados).map(assento => assento.dataset.assento);

            if (nomesDosAssentos.length > 0) {
                listaAssentosEl.textContent = nomesDosAssentos.join(', ');
            } else {
                listaAssentosEl.textContent = 'Nenhum';
            }
        }
    }
});