from bottle import request
from types import SimpleNamespace
from .controlador_base import ControladorBase
from models import Voo, User, Reserva, Pagamento
from data.database import get_db
from sqlalchemy.orm.attributes import flag_modified

class ControladorPagamento(ControladorBase):
    """Controller para gerenciar o processo de checkout e finalização da compra."""
    def __init__(self, app):
        """Recebe as instâncias compartilhadas de todos os models necessários."""
        super().__init__(app)
        self.configurar_rotas()

    def configurar_rotas(self):
        """Mapeia as URLs de pagamento para os métodos."""
        self.app.route('/pagamento/<id_voo>/<assentos_selecionados>', method='GET', callback=self.pagina_pagamento)
        self.app.route('/pagamento/<id_voo>/<assentos_selecionados>', method='POST', callback=self.efetuar_pagamento)

    def pagina_pagamento(self, id_voo, assentos_selecionados):
        """Apenas prepara e exibe os dados para a página de confirmaçaõ,
        antes de o usuário inserir os dados do cartão."""
        db = next(get_db())
        voo = db.query(Voo).filter(Voo.numero_voo == id_voo).first()
        if not voo:
            return "Voo não encontrado!"

        lista_assentos = assentos_selecionados.split(',')
        
        # Prepara um objeto de resumo para ser usado pelo template.
        dados_reserva = {
            'voo': voo,
            'assentos': lista_assentos,
            'custo': {
                'total': voo.preco * len(lista_assentos)
            }
        }
        
        # Converte o dicionário em um objeto para o template usar
        reserva_objeto = SimpleNamespace(**dados_reserva)
        
        return self.renderizar('pagamento', reserva=reserva_objeto, titulo="Pagamento")

    def efetuar_pagamento(self, id_voo, assentos_selecionados):
        """É chamado quando o usuário submete o formulário de pagamento.
        Cria as Resercas e o Pagamento no Sistema."""
        db = next(get_db())
        # Verifica se há um usuário logado.
        id_usuario_logado = self.obter_usuario_logado()
        if not id_usuario_logado:
            return self.redirecionar('/login', erro="Você precisa estar logado para completar a compra.")

        # Bysca os objetos de Usuário e Voo..
        usuario = db.query(User).filter(User.id == id_usuario_logado).first()
        voo = db.query(Voo).filter(Voo.numero_voo == id_voo).first()

        # Lógica para criar uma reserva para cada assento.
        reservas_criadas = []
        lista_assentos = assentos_selecionados.split(',')
        
        assentos_ocupados = voo.assentos_ocupados

        for assento in lista_assentos:
            # Lógica de verificação e reserva do assento
            if assento in assentos_ocupados:
                db.rollback()
                return f"Erro: O assento {assento} já está reservado."

            assentos_ocupados.append(assento)

            # Cria a instância da Reserva.
            nova_reserva = Reserva(
                user=usuario,
                voo=voo,
                assento=assento,
                status="Confirmada"
                )
            db.add(nova_reserva)
            reservas_criadas.append(nova_reserva)

        # Salva o estado do voo com os novos assentos ocupados.
        voo.assentos_ocupados = assentos_ocupados
        flag_modified(voo, "assentos_ocupados")
        db.add(voo)

        # Cria a instância do Pagamento.
        pagamento = Pagamento(
            reserva=reservas_criadas[0],  # Associa o pagamento à primeira reserva
            valor=voo.preco * len(reservas_criadas),
            forma_pagamento='Cartão de Crédito'
            )
        db.add(pagamento)
        
        db.commit()

        # Renderiza a página de sucesso.
        return self.renderizar('pagamento_sucesso', valor=pagamento.valor,quantidade=len(reservas_criadas), titulo="Pagamento Efetuado")