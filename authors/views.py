# pylint: disable=all
# flake8: noqa
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def register_view(request):
    # aqui estamos trafegando os dados do POST que veio de register_create
    # usamos o mesmo nome da criação do dict
    # passamos o bound form se existir para dentro do form
    # caso não exista vai renderizar um novo
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    # vamos trafegar dados entre páginas e para isso vamos usar session de usuarios
    if not request.POST:
        raise Http404()

    # estamos enviando os dados para session
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    if form.is_valid():
        # se quiser pegar dados
        # data = form.save()
        # aqui estamos pegando os dados do save
        user = form.save(commit=False)
        # editamos o password
        user.set_password(user.password)
        user = form.save()
        messages.success(request, 'Your user is created, please log in')
        
        # deletando chave de um dict
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


# so vamos fazer o match dos dados
def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        # autenticando usuario
        authenticated_user = authenticate(
            # quero o usuario, se não tiver passamos uma string vazia
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        
        if authenticated_user is not None:
            messages.success(request, 'You are now authenticated')
            login(request, authenticated_user)
            return redirect(login_url)
        messages.error(request, 'Invalid credentials')
        return redirect(login_url)
    messages.error(request, 'Invalid username or password')
    return redirect(login_url)


# redirect_field_name é um redirecionamento para o lugar onde estava anteriormente
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    # criado login via form por segurança para uso do CSRF
    # duas barreiras de segurança
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    return render(request, 'authors/pages/dashboard.html')


# quando o formulário possui dados é chamado de BOUND

# session registra o id do navegador, para salvar um cookie com seu id
# estamos captando a quantidade de vezes acessado pelo user
# estamos checando se não tiver vai se 1 (or 1)
# pode ser acessado diretamente dentro do template
# request.session['number'] = request.session.get('number') or 1
# request.session['number'] += 1