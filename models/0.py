from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Inventario Forestal Nacional'
settings.subtitle = ''
settings.author = 'Ingesur SRL'
settings.author_email = 'contacto@ingesur.com.uy'
settings.keywords = ''
settings.description = 'Aplicaci\xc3\xb3n que modela el Inventario Forestal Nacional de la Direcci\xc3\xb3n General Forestal.'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.db'
settings.security_key = '4e773d36-53e7-4758-a323-635465686c4e'
settings.email_server = 'logging'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = ['']

### Definicion de variabels globales de la aplicacion
## Tipos de reporte (tabla TipoReporte)
CON_INFORMACION=1
NO_BOSQUE=2
BOSQUE_CORTADO=3
NO_INGRESO=4
