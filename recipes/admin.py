from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


# esse decoration é a mesma coisa que colocar o link admin.site
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # demonstra as colunas la no admin
    list_display = ['id', 'title', 'created_at', 'author', 'is_published',]

    # inserir links nas colunas especificadas
    list_display_links = ['id', 'title',]

    # inserir campo de search
    search_fields = ['id', 'title', 'description', 'created_at', 'is_published']

    # inserindo filtros
    list_filter = ['id', 'title', 'description', 'created_at', 'is_published']

    # limitando a quantidade de objetos por pagina
    list_per_page = 10

    # inserir campos editaveis, tem que está inserido no list_display
    list_editable = ['is_published',]

    # ordenando os campos, sinal negativo para DESC
    ordering = ['-id',]

    # indicando um campo com auto preenchimento
    # essa opção é um dict
    prepopulated_fields = {
        "slug": ('title',)
    }


admin.site.register(Category, CategoryAdmin)
