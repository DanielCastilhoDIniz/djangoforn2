from django.db import models
from stdimage.models import StdImageField


# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify


class Base(models.Model):
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    modificado = models.DateTimeField('Modificado em', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Product(Base):
    name = models.CharField('Nome', max_length=100)
    price = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    stock = models.IntegerField('Estoque')
    image = StdImageField('Imagem', upload_to='products',
                          variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True,
                            editable=False)
    description = models.TextField('Descrição', blank=True)

    def __str__(self):
        return self.name


def product_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.name)


signals.pre_save.connect(product_pre_save, sender=Product)
