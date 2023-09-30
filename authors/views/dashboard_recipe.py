from django.views import View
from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from recipes.models import Recipe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Class Based Views
# familia de classes separadas por métodos http
@method_decorator(
    login_required(
        login_url="authors:login",
        redirect_field_name="next",
    ),
    # aqui esto decorando um função que está dentro da classe View
    name="dispatch",
)
class DashboardRecipe(View):
    # estou subscrevendo o método
    def __init__(self, *args, **kwargs):
        # mas ainda assim chamo o método anterior
        super().__init__(*args, **kwargs)

    # subscrevendo outro método
    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    # método de extração
    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )

    # esse é uma forma de decorar algo especifico
    # @method_decorator(
    #     login_required(
    #         login_url="authors:login",
    #         redirect_field_name="next",
    #     )
    # )

    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        # como é um get so precisa instacia-lo
        # usamos para demostrar no form uma instancia de um recipe
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        # aqui está recebendo os dados
        # e no caso a instancia está recebendo uma recipe
        # quando o usuario salvar o form ele vai salvar no instance
        # quando temos arquivos no nosso form é necessario manipula-los
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            # agora o form é valido e eu posso tentar salvar
            # aqui estamos fazendo um salve fake
            # estamos salvando os dados no recipe
            recipe = form.save(commit=False)
            # confirmando que o author é dono do recipe
            recipe.author = request.user
            # nunca vai ser possivel enviar HTML
            recipe.preparation_steps_is_html = False
            # verificar se foi publicado
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            # quando formos salvar é necessario capturar o id da receita
            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
            )

        return self.render_recipe(form)


@method_decorator(
    login_required(
        login_url="authors:login",
        redirect_field_name="next",
    ),
    # aqui esto decorando um função que está dentro da classe View
    name="dispatch",
)
class DashboardRecipeDelete(DashboardRecipe):
    # aqui colocamos args e kwarg para recebermos e manipularmos via argumentos
    def post(self, *args, **kwargs):
        # estamos pegando o id do form
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))
