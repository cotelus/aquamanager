class ContadorController():
    def __init__(self, db=None):
        self.name = "Controlador de contadores - SINGLETON -"
        self.contadores = [{'nombre':'Contador 1', 'valor': 2}, {'nombre':'Contador 2', 'valor': 6}]

    """
        Devuelve una lista de contadores
    """
    async def get_list(self):
        return self.contadores 
