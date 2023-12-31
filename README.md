# Django installation
> python3 -m venv venv
> python3 -m pip install pip setuptools wheel --upgrade
> . venv/bin/activate
> pip install django
> criar arquivo de debugger

# Processo Django
> criar template
> criar view
> criar url
> tratar css
> tratar cados

> # Django commands
>> ##### runserver 
>> - inicializando servidor django
>
>> ##### makemigrations 
>> - criando models de tabela
>
>> ##### migrate 
>> - persistindo tabelas no banco de dados
>
>> ##### inspectdb 
>> - criar model de uma tabela ja existente
>
>> ##### sqlflush 
>> - apagando os dados do banco de dados e cache do django
>
>> ##### flush 
>> - apagando dados cache do django
>
>> ##### shell 
>> - terminal do django
>
>> ##### startapp 
>> - iniciando aplicativo
>
>> ##### startproject 
>> - iniciando projeto
>
>> ##### test 
>> - executar testes padrões do Django
>
>> ##### check
>
>> ##### compilemessages
>
>> ##### createcachetable
>
>> ##### dbshell
>
>> ##### diffsettings
>
>> ##### dumpdata
>
>> ##### loaddata
>
>> ##### makemessages
>
>> ##### optimizemigration
>
>> ##### sendtestemail
>
>> ##### showmigrations
>
>> ##### sqlmigrate
>
>> ##### sqlsequencereset
>
>> ##### squashmigrations
>
>> ##### testserver
>---

> # Terminal Unix Commands
>> ##### consultar processador do pc
>> - sysctl -n machdep.cpu.brand_string 
>---

> # Info Django
>> ##### *args e **kwargs
>> - *args tem que ser informado os dados em ordem, por exemplo um id, tem que ser em sequencia.
>> - **kwargs temos que passar um dicionario com as informações.
>
>> ##### resolve()
>> - função do Django que manipula URL, resolve o caminho da url trazendo como argumentos informações sobre a url chamado de ResolverMatch, e esse objeto contém varios detalhes sobre a URL correspondente incluindo a função de visualização a view ('func')
>
>> ##### querystring
>> - usado para inserir pares de chave e valor
>> - na url apos o '?' é tudo uma query string
>> - url/?search=qualquervalor&query=qualquervalor
>> - so vem no método GET
>
>> ##### tag form
>> - action na tag corresponde o redirecionamento da url
>> - method é o método que vamos utilizar, para query string sempre GET
>> - name é o paramêtro que utilizamos para mostrar apartir de qual caracter na url é uma query string, para identificar
>> - required usado para forçar o usuario a digitar um valor
>
>> ##### safe
>> - | safe
>> - usamos o pipe safe no template para que o Django renderize html do lado client
>
>> ##### quebrar linha
>> - option + z
>---

##### Arquivos Statics
- Nos arquivos HTML usamos a tag load static


##### Jinja do Django
- Quando fazemos um for dentro de uma página que renderiza outro template esse template recebe como parametro os dados contidos no for.


##### Filtros do Django para Jinja
- Verifique a documentação
- usamos pipe ('|') dentro das {{ }} para indicar o uso de filtros


##### Atualizando cache página
- cmd + Shift + R


##### Usando Shell do Django
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


##### Como renomear um projeto Django
    - Necessário mudar em todos os arquivos que possui o nome do seu projeto
    - Pesquisaremos em todos os arquivos de uma vez
        - Vamos na lupa e pesquisaremos pelo nome e Replace


##### Traduzindo páginas do Django
    - LANGUAGE_CODE = 'pt-br'
    - TIME_ZONE = 'America/Sao_Paulo'


##### Autopep/ Flake8/ MyPy/ PyLint
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


##### Tipos de testes
= unitarios
= funcionais
= integração


##### Testes
- pip install pytest pytest-django
- pip install parameterized (testes multiplos no for)
- pip install pytest-watch
- pip install coverage
- podemos escrever test no arquivo test.py
= no terminal do mac
    - ativamos o venv
    = executamos 
        - pytest
    = executar mostrando prints
        - pytest -rP
    = comando padrao Django
        - python manage.py test
    = pytest-watch
        - usamos para que o terminal execute automaticamente todo test
        - comando ptw
    = executar um unico test usando -k como busca
        - pytest -k 'nome da variável'
        - pwt -- -k 'nome da variável'
= debug console
    - colocamos o breakpoint após o código que queremos
    - executamos o test pelo play com debug
    = comando para ver paramêtros que podemos acessar
        - dir(nome da váriavel)
= realtórios de testes
    - usamos o coverage
    - branchs é quando temos mais de uma possibilidade na função e tem que ser testada
    - criar arquivo .coveragerc
    - coverage run --omit='*/venv/*' -m pytest
    - coverage run -m pytest
    = gerando html
        - coverage html


##### Teste Unitarios
= usamos o test do Django para faze-los
= comandos
    - python manage.py test
    - python manage.py test -v3 (para verbosidade, que é + detalhes exibidos)
    - python manage.py test -k 'nome da váriavel'


##### Teste PyTests
= somente pytest vai entender essas marcações
= depois de criado o marker no pytest.ini, inserir na parte do test decorator
    = esse comando vai executar somente os testes que possuir esse marker
    = posso inserir na classe, ou em uma função especifica
        - pytest -m 'functional_test' -rP 
        - pytest -m 'not functional_test' -rP
    = executar um pytest unico
        - pytest -k 'nome_do_test'
= carregar arquivo .env
    - pip install pytest-dotenv


##### Criando chaves criptograficas
- python -c "import string as s;from random import SystemRandom as sr;print(''.join(sr().choices(s.ascii_letters + s.punctuation, k=64)))"


##### Mixins
= Padrão de projeto, onde criamos um saco de classes
= Cuidados com as heranças de classes e atributos
= Usamos mixins para adicionar métodos em outras classes


##### Class Based Views
> Aqui teremos o método dispatch
    - ele tenta encontrar o método do http para buscar a classe correta
    - levantamento de erros ja possuem na CBV

> Views de base
    - são heranças que podem ser repassadas a outras CBV
    - verificar documentação para verificar a ancestralidade de métodos
    - a descrição dos métodos está na documentação
    - https://docs.djangoproject.com/pt-br/4.2/topics/class-based-views/
    - https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/

##### Deploy
Título
Deploy, Hospedagem e domínio e opções inclusivas para todos

Domínio e hospedagem: guia para leigos
https://www.otaviomiranda.com.br/2018/dominio-e-hospedagem-guia-para-leigos/

Heroku
https://www.heroku.com/

VirtualBox Tutorial
https://www.youtube.com/watch?v=Vl6f8_vin9M

Digital Ocean
https://www.digitalocean.com/pricing/

Google Cloud Platform
https://cloud.google.com/

Aws
https://aws.amazon.com/pt/

UTM
https://mac.getutm.app/

> Criando ssh key para o google
    - ssh-keygen -t rsa -b 4096 -f CAMINHO+NOME_DA_CHAVE

> Para conectar-se ao servidor usando uma chave SSH com caminho personalizado, utilize:
    - ssh IP_OU_HOST -i CAMINHO+NOME_DA_CHAVE

> Ao entrar no servidor
> A primeira coisa será atualizar tudo:

    - sudo apt update -y
    - sudo apt upgrade -y
    - sudo apt autoremove -y
    - sudo apt install build-essential -y
    - sudo apt install python3.9 python3.9-venv python3.9-dev -y
    - sudo apt install nginx -y
    - sudo apt install certbot python3-certbot-nginx -y
    - sudo apt install postgresql postgresql-contrib -y
    - sudo apt install libpq-dev -y
    - sudo apt install git

> Instalando o PostgreSQL
    - sudo apt install postgresql postgresql-contrib -y
    - Caso queira mais detalhes: https://youtu.be/VLpPLaGVJhI
    - Mais avançado: https://youtu.be/FZaEukN_raA

    - Configurando POSTGRESQL
        - sudo -u postgres psql

        - Criando um super usuário
            CREATE ROLE usuario WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'senha';

        - Criando a base de dados
            CREATE DATABASE basededados WITH OWNER usuario;

        - Dando permissões
            GRANT ALL PRIVILEGES ON DATABASE basededados TO usuario;

        - Saindo
            \q

        - sudo systemctl restart postgresql

        Caso queira mais detalhes: https://youtu.be/VLpPLaGVJhI
        Mais avançado: https://youtu.be/FZaEukN_raA

> Configurando o git
    - git config --global user.name 'Seu nome'
    - git config --global user.email 'seu_email@gmail.com'
    - git config --global init.defaultBranch main

    - Criando um repositório no servidor
        Um repositório bare é um repositório transitório (como se fosse um github).
        - mkdir -p ~/app_bare
        - cd ~/app_bare
        - git init --bare
        - cd ~
    
    - Criando o repositório da aplicação
        - mkdir -p ~/app_repo
        - cd ~/app_repo
        - git init
        - git remote add origin ~/app_bare
        - git add . && git commit -m 'Initial'
        - cd ~

    - No seu computador local, adicione o bare como remoto:
        - git remote add app_bare cursodjangoserver:~/app_bare
        - git push app_bare <branch>

    - No servidor, em app_repo, faça pull:
        - cd ~/app_repo
        - git pull origin <branch>

> Criando o ambiente virtual
    - cd  ~/app_repo
    - git pull origin <branch>
    - python3.9 -m venv venv
    - . venv/bin/activate
    - pip install -r requirements.txt
    - pip install psycopg2
    - pip install gunicorn

> Apontando para domínio
    Pega ip do servidor, vá até o DNS do hospedador do domínio.
    Cria um registro 
        - {nome}.{domínio} vai apontar para {IPv4}
        - Tipo A
        - Nome
        - IPv4
        - Se incluir proxy ele vai alterar o IP, vai mascarar o ip por segurança
    
    No computador
        - ping {dominio completo}

> Atualizando versão app no server
    - roda os testes primeiramente após a edição
    - enviar ao repositorio bare
    - fazer o pull
    - restart no socket do gunicorn
        - sudo systemctl restart {socket}
    
    - diretamente do terminal do pc
        - ssh {nome do servidor} 'cd ~/app_repo ; git pull origin main ; venv/bin/python manage.py makemigrations ; venv/bin/python manage.py migrate ; sudo systemctl restart {socket} ; sudo systemctl restart nginx ;'

> Criando uma API
    - Usaremos o Django padrão para gerar

> Django DebugToolBar
    - https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#install-the-package

> Optimizando DB
    - Usamos uma função para o model do Django
        - 1 para N ou 1 para 1
            - OneToOneField()
            - ForeignKey
                - select_related({campo1}, {campo2})
        - N para N
            - ManyToManyField()
            - foreignKey
                - prefetch_related({campo1}, {campo2})

> Manipulação via shell
- from recipes.models import Recipe
- r = Recipe.objects.all().last()
- r.tags.all()
- r.tags.filter(name__icontains='teste')
- r.tags.last() ou first()
- r.tags.create(name='mais uma tag)
- r.tags.filter(name__icontains='teste').delete()

fazendo clone
- r.id = None; r.slug='novo'; r.save()
- t = Tag.objects.create(name='essa é nova', content_object=r)