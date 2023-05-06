class ContadorController():
    def __init__(self, db=None):
        self.name = "Controlador de contadores - SINGLETON -"
        self.contadores = {'Contador1': 2, 'Contador2': 3}

    """
        Devuelve una lista de contadores
    """
    async def get_list(self):
        return self.contadores 
