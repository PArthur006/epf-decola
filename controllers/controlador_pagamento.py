# controllers/controlador_pagamento.py (VERSÃO CORRIGIDA)

from bottle import request
from .controlador_base import ControladorBase
# Importa o SimpleNamespace, que converte dicionários em objetos
from types import SimpleNamespace
from models.voo import VooModel
from models.user import UserModel
from models.reserva import ReservaModel, Reserva
from models.pagamento import PagamentoModel, Pagamento

class ControladorPagamento(ControladorBase):
    def __init__(self, app, user_model: UserModel, voo_model: VooModel, reserva_model: ReservaModel, pagamento_model: PagamentoModel):
        super().__init__(app)
        self.user_model = user_model
        self.voo_model = voo_model
        self.reserva_model = reserva_model
        self.pagamento_model = pagamento_model
        self.configurar_rotas()

    def configurar_rotas(self):
        self.app.route('/pagamento/<id_voo>/<assentos_selecionados>', method='GET', callback=self.pagina_pagamento)
        self.app.route('/pagamento/<id_voo>/<assentos_selecionados>', method='POST', callback=self.efetuar_pagamento)

    def pagina_pagamento(self, id_voo, assentos_selecionados):
        voo = self.voo_model.get_by_numero_voo(id_voo)
        if not voo:
            return "Voo não encontrado!"

        lista_assentos = assentos_selecionados.split(',')
        
        # Cria um dicionário com os dados
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
      id_usuario_logado = self.obter_usuario_logado()
      if not id_usuario_logado:
          return self.redirecionar('/login', erro="Você precisa estar logado para completar a compra.")

      usuario = self.user_model.get_by_id(id_usuario_logado)
      voo = self.voo_model.get_by_numero_voo(id_voo)
      reservas_criadas = []

      for assento in assentos_selecionados.split(','):
          if assento in voo.assentos_ocupados:
             return f"Erro: O assento {assento} já está reservado."

          sucesso = voo.reservar(assento)  # Aqui você chama seu método reservar correto
          if not sucesso:
              return f"Erro ao reservar o assento {assento}."

          id_reserva_nova = f"R{voo.numero_voo}{usuario.id}{assento}"

          nova_reserva = Reserva(
              id_reserva=id_reserva_nova,
              user=usuario,
              voo=voo,
              assento=assento,
              status="Confirmada"
            )
          self.reserva_model.add(nova_reserva)
          reservas_criadas.append(nova_reserva)

      # Salva o estado atualizado do voo
      self.voo_model.update(voo)

      pagamento = Pagamento(
         id_pagamento=None,
         reserva=reservas_criadas[0],  # Associa o pagamento à primeira reserva
         valor=voo.preco * len(reservas_criadas),
         forma_pagamento='Cartão de Crédito'
        )
      self.pagamento_model.add(pagamento)

      return self.renderizar('pagamento_sucesso', valor=pagamento.valor,quantidade=len(reservas_criadas),
                             titulo="Pagamento Efetuado")

