# pylint: disable=all
# flake8: noqa

from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

def register_view(request):
    # aqui estamos trafegando os dados do POST que veio de register_create
    # usamos o mesmo nome da criação do dict
    # passamos o bound form se existir para dentro do form
    # caso não exista vai renderizar um novo
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:create'),
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

    return redirect('authors:register')


# quando o formulário possui dados é chamado de BOUND

# session registra o id do navegador, para salvar um cookie com seu id
# estamos captando a quantidade de vezes acessado pelo user
# estamos checando se não tiver vai se 1 (or 1)
# pode ser acessado diretamente dentro do template
# request.session['number'] = request.session.get('number') or 1
# request.session['number'] += 1