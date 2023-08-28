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

# Usando Shell do Django
- python manage.py shell
    - aqui posso verificar comandos de query entre outros.
    - aqui podemos verificar como está a execução de determinado código
- comandos shell
    = para eu ver os campos disponíveis
        - recipe._meta.get_fields()
    = para ver um indice especifico
        - recipe._meta.get_fields()[0]
    = para ver o nome do campo
        - recipe._meta.get_fields()[0].name
    = para ver o valor dentro do campo
        - getattr(recipe._meta.get_fields()[0])
        - recipe.id
    = para selecionar um objeto direto
        - categories = Category.objects.get(id=1)
    = cadastrando user
        - from django.contrib.auth.models import User
        - User.objects.create_user(first_name='NOME', last_name='SOBRENOME', username='USER', email='EMAIL', password='PASSWORD')
    = consultando uma função
        - from recipes.models import Recipe
        - recipes = Recipe.objects.filter(
            category__id=(category_id),
            is_published=True,
        ).order_by('-id')
        return render(request, 'recipes/pages/category.html', context={
            'recipes': recipes,
        })
        = no shell
            - recipes.first().category.name
            - no código acima usamos a função first para pegar o primeiro elemento do query set, e temos então um objeto e dele eu quero a category que é um model com foreignKey no model Recipes, e devido a essa ligação temos acesso ao name do category.

# Como renomear um projeto Django
    - Necessário mudar em todos os arquivos que possui o nome do seu projeto
    - Pesquisaremos em todos os arquivos de uma vez
        - Vamos na lupa e pesquisaremos pelo nome e Replace

# Traduzindo páginas do Django
    - LANGUAGE_CODE = 'pt-br'
    - TIME_ZONE = 'America/Sao_Paulo'

# Autopep/ Flake8/ MyPy/ PyLint
    = pip install mypy
        = comando para verificar um arquivo
            -mypy nome-arquivo.py
    = pip install pylint-django
        = para gerar arquivo .pylintrc
            - pylint --generate-rcfile > .pylintrc
    = pip install flake8
        = comando para verificar todos erros em todos arquivos
            - flake8 
    - pip install autopep8
    - MyPy = usuado para tipagem

    ```
        {
        "python.languageServer": "Pylance", // ms-python.vscode-pylance
        "python.testing.unittestEnabled": false, // ms-python.python
        "python.testing.pytestEnabled": true,
        "python.testing.pytestArgs": [], // -x to bail
        "flake8.args": ["--config=.flake8"],
        "flake8.importStrategy": "fromEnvironment",
        "pylint.args": ["--rcfile=.pylintrc"],
        "pylint.importStrategy": "fromEnvironment",
        "mypy-type-checker.args": ["--config-file=mypy.ini"],
        "mypy-type-checker.importStrategy": "fromEnvironment",
        "autopep8.args": ["--config", "setup.cfg"],
        "autopep8.importStrategy": "fromEnvironment",
        "python.defaultInterpreterPath": "venv/bin/python",
        "[python]": {
            "editor.defaultFormatter": "ms-python.autopep8", // ms-python.python
            "editor.tabSize": 4,
            "editor.insertSpaces": true,
            "editor.formatOnSave": true,
            "editor.formatOnType": true,
            "editor.codeActionsOnSave": {
            "source.organizeImports": true
            }
        },
        "[html]": {
            "editor.formatOnSave": true,
            "editor.defaultFormatter": "vscode.html-language-features",
            "editor.quickSuggestions": {
            "other": true,
            "comments": true,
            "strings": true
            }
        },
        "[django-html]": {
            "editor.formatOnSave": false,
            "editor.defaultFormatter": "vscode.html-language-features",
            "editor.quickSuggestions": {
            "other": true,
            "comments": true,
            "strings": true
            }
        },
        "files.associations": {
            "*.js": "javascript",
            "*.jsx": "javascriptreact",
            "*.xml": "html",
            "*.svg": "html",
            "*.html": "html",
            "django-html": "html", // batisteo.vscode-django
            "**/*.html": "html",
            "**/templates/**/*.html": "django-html",
            "**/base_templates/**/*.html": "django-html",
            "**/requirements{/**,*}.{txt,in}": "pip-requirements"
        },
        "emmet.includeLanguages": {
            "django-html": "html", // batisteo.vscode-django
            "javascript": "javascriptreact",
            "typescript": "typescriptreact"
        }
        }
    ```

# Testes
- pip install pytest pytest-django