# guarda datos
class MySQLConfig:
    # servidor
    HOST = 'localhost'
    
    # Usuario
    USER = 'root'
    
    # Contraseña
    PASSWORD = ''
    
    # Nombre
    DATABASE = 'biblioteca_virtual'
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'