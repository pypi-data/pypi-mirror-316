class DatabaseFacade:
    """
        Fachada de base de datos, crea conexion con un singleton a mssql, y define las operaciones dentro de esta como funciones independientes
    """
    def __init__(self, connection_string: str):
        self.connection_string: str = connection_string
        # self.db = Singleton(connection_string)
        
    def connection_string(self) -> str:
        return self.connection_string
