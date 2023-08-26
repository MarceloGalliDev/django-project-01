# Django installation
> python3 -m venv venv
> python3 -m pip install pip setuptools wheel --upgrade
> . venv/bin/activate
> pip install django
> criar arquivo de debugger

# Django commands
> check
> compilemessages
> createcachetable
> dbshell
> diffsettings
> dumpdata
> flush
> inspectdb
> loaddata
> makemessages
> makemigrations = criando models de tabela
> migrate = persistindo tabelas no banco de dados
> optimizemigration
> runserver = inicializando servidor django
> sendtestemail
> shell = terminal do django
> showmigrations
> sqlflush = apagando os dados do banco de dados e cache do django
> sqlmigrate
> sqlsequencereset
> squashmigrations
> startapp = iniciando aplicativo
> startproject = iniciando projeto
> test
> testserver

# Arquivos Statics
- Nos arquivos HTML usamos a tag load static

# Jinja do Django
- Quando fazemos um for dentro de uma página que renderiza outro template esse template recebe como parametro os dados contidos no for.

# Filtros do Django para Jinja
- Verifique a documentação
- usamos pipe ('|') dentro das {{ }} para indicar o uso de filtros

# Atualizando cache página
- cmd + Shift + R