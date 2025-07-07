// Aguarda todo o conteúdo do HTML ser carregado antes de executar qualquer script.
// Isso garante que todos os elementos que o JavaScript procura já existem na página.
document.addEventListener('DOMContentLoaded', function() {

    // LÓGICA DO CARROSSEL DE PACOTES (Página Inicial)
    const containerPacotes = document.getElementById('containerPacotes');
    
    // Garante que o código do carrossel só rode se os elementos existirem na página atual.
    if (containerPacotes) {
        // Seleciona os botões de navegação do carrossel.
        const btnAnterior = document.getElementById('btnAnterior');
        const btnProximo = document.getElementById('btnProximo');
        
        // Verifica se todos os componentes do carrossel estão presentes.
        if (btnAnterior && btnProximo) {
            // Calcula o quanto rolar (largura de um card + o espaço de 'gap').
            const tamanhoScroll = containerPacotes.querySelector('.cartao').offsetWidth + 20;

            // Adiciona o evento de clique para o botão "Próximo".
            btnProximo.addEventListener('click', () => {
                containerPacotes.scrollBy({
                    left: tamanhoScroll,
                    behavior: 'smooth'
                });
            });

            // Adiciona o evento de clique para o botão "Anterior".
            btnAnterior.addEventListener('click', () => {
                containerPacotes.scrollBy({
                    left: -tamanhoScroll,
                    behavior: 'smooth'
                });
            });
        }
    }

    // LÓGICA DE MOSTRAR/OCULTAR SENHA (Páginas de Login e Cadastro)
  
    // Função genérica e reutilizável para alternar a visibilidade de qualquer campo de senha.
    function configurarToggleSenha(idCampo, idToggle) {
        const campoSenha = document.getElementById(idCampo);
        const botaoToggle = document.getElementById(idToggle);

        // Adiciona o evento de clique apenas se ambos, campo e botão, forem encontrados.
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


    // LÓGICA DE EXPANDIR CARD DE VOO (Página de Lista de Voos)

    const cartoesVoo = document.querySelectorAll('.cartao-voo-interativo');

    // Garante que o código só rode se houver cards de voo na página.
    if (cartoesVoo.length > 0) {
        // Para cada card encontrado, adiciona um evento de clique.
        cartoesVoo.forEach(cartao => {
            cartao.addEventListener('click', () => {
                // Adiciona ou remove a classe 'esta-expandido' no card clicado.
                cartao.classList.toggle('esta-expandido');
            });
        });
    }

    // SEÇÃO 4: LÓGICA DA PÁGINA DE SELEÇÃO DE ASSENTOS

    const mapaAssentos = document.querySelector('.mapa-assentos');

    // Garante que o código só rode se estiver na página do mapa de assentos.
    if (mapaAssentos) {
        // Seleciona os elementos do rodapé para atualização.
        const listaAssentosEl = document.getElementById('listaAssentosSelecionados');
        const botaoPagarEl = document.getElementById('botaoPagar');
        
        // Adiciona um único "escutador" de clique no contêiner pai dos assentos.
        mapaAssentos.addEventListener('click', function(event) {
            const elementoClicado = event.target;

            // Verifica se o elemento clicado é de fato um assento e se está disponível.
            if (elementoClicado.classList.contains('assento') && elementoClicado.classList.contains('disponivel')) {
                elementoClicado.classList.toggle('selecionado');
                atualizarResumoAssentos();
            }
        });

        // Adiciona o evento de clique ao botão "Pagar".
        botaoPagarEl.addEventListener('click', function() {
            // Pega a lista de nomes dos assentos atualmente selecionados.
            const assentosSelecionados = document.querySelectorAll('.assento.selecionado');
            // Extrai apenas os nomes dos assentos.
            const nomesDosAssentos = Array.from(assentosSelecionados).map(assento => assento.dataset.assento);
            
            // Validação simples para não permitir avançar sem assentos.
            if (nomesDosAssentos.length === 0) {
                alert('Por favor, selecione pelo menos um assento.');
                return; // Para a execução se nenhum assento foi selecionado
            }

            // Pega o ID do voo da URL atual para construir a próxima URL
            const urlPath = window.location.pathname.split('/');
            const idVoo = urlPath[urlPath.length - 1];
            
            // Constrói a URL final para a página de pagamento e redireciona o usuário
            const urlDestino = `/pagamento/${idVoo}/${nomesDosAssentos.join(',')}`;
            console.log("Redirecionando para:", urlDestino);
            window.location.href = urlDestino;
        });

        // Função auxiliar para ler os assentos selecionados e atualizar o texto no rodapé.
        function atualizarResumoAssentos() {
            const assentosSelecionados = document.querySelectorAll('.assento.selecionado');
            const nomesDosAssentos = Array.from(assentosSelecionados).map(assento => assento.dataset.assento);

            // Atualiza o texto com base na quantidade de assentos selecionados.
            if (nomesDosAssentos.length > 0) {
                listaAssentosEl.textContent = nomesDosAssentos.join(', ');
            } else {
                listaAssentosEl.textContent = 'Nenhum';
            }
        }
    }
});