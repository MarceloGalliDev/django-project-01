import string
from random import SystemRandom
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # vamos usar slug como id

    # aqui estamos criando models genericos
    # pois nao vamos atrelar a nenhum outro app

    # aqui começa os campos para relação genérica
    # content_type ele vai representar um model que queremos encaixar aqui
    # ex: recipe, authors
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # object_id representa o id da linha do model descrito acima
    # documentação sugere usarmos PositiveIntegerField()
    # vamos usar CharField pelo fato de outros DB serem impactados
    object_id = models.CharField(max_length=255)

    # vamos informar a relações genérica que conhece os campos acima
    # content_type e object_id
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        # aqui vamos retornar uma lista com dados randomicos
        # 5 letras de A a Z e de 0 a 9
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
