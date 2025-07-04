from datetime import datetime

class Pagamento:
    def __init__(self, id_pagamento, numero_voo, valor, forma_pagamento, status, data_pagamento=None):
        self.id_pagamento = id_pagamento
        self.numero_voo = numero_voo
        self.valor = valor
        self.forma_pagamento = forma_pagamento  # Ex: 'Cartão', 'PIX', 'Boleto'
        self.status = status                    # Ex: 'Pendente', 'Pago', 'Cancelado'
        self.data_pagamento = data_pagamento or datetime.now()

    def __repr__(self):
        return (f"Pagamento(id_pagamento={self.id_pagamento}, numero_voo='{self.numero_voo}', "
                f"valor={self.valor}, forma_pagamento='{self.forma_pagamento}', "
                f"status='{self.status}', data_pagamento='{self.data_pagamento}')")