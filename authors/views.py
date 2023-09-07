from django.shortcuts import render
from .forms.forms import RegisterForm


def register_view(request):
    if request.POST:
        # quando o formulário possui dados é chamado de BOUND
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })
