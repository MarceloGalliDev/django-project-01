# flake8: noqa
# pylint: disable=all
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=64)
    
    # aqui é usado para página de admin
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    # usado para fazer uma espécie de mask na url
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # especificamos o caminho que vamos receber a imagem, criando as pastas dinamicamente por data
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    # na foreignKey especificamos que quando deletar setamos como null(null = None)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    # esse campo puxamos diretamente do models User padrão do Django
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
    # adicionando o botão no django admin para visualização da página
    # podemos inserir essa função diretamente no template desde que ja esteja salvo a recipe
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))
    
    # acessando os campos de model
    # slugfy cria uma slug a partir de um texto
    # estamos adicionando uma slug no objeto
    # o django ja salva o método
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)