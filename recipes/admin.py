from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericStackedInline
# from tag.models import Tag

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


# class TagInline(GenericStackedInline):
#     model = Tag
#     fields = 'name',
#     extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at',
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps',
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html',
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',)
    }

    # autocomplete para foreign_key ou many_to_many
    # no caso entre recipe e tags
    # se usarmos assim temos que ter o relacionamento
    autocomplete_fields = 'tags',

    # inlines = [
    #     TagInline,
    # ]


admin.site.register(Category, CategoryAdmin)


# # demonstra as colunas la no admin
# list_display = ['id', 'title', 'created_at', 'author', 'is_published',]

# # inserir links nas colunas especificadas
# list_display_links = ['id', 'title',]

# # inserir campo de search
# search_fields = ['id', 'title', 'description', 'created_at', 'is_published']

# # inserindo filtros
# list_filter = ['id', 'title', 'description', 'created_at', 'is_published']

# # limitando a quantidade de objetos por pagina
# list_per_page = 10

# # inserir campos editaveis, tem que está inserido no list_display
# list_editable = ['is_published',]

# # ordenando os campos, sinal negativo para DESC
# ordering = ['-id',]

# # indicando um campo com auto preenchimento
# # essa opção é um dict
# prepopulated_fields = {
#     "slug": ('title',)
# }
