from cache_toolbox import cache_model, cache_relation

from django.db import models

class Foo(models.Model):
    bar = models.TextField()

class Bazz(models.Model):
    foo = models.OneToOneField(
        Foo,
        related_name='bazz',
        on_delete=models.CASCADE,
    )

    value = models.IntegerField(null=True)

cache_model(Foo)
cache_relation(Foo.bazz)

class MultipleForeignKey(models.Model):
    name = models.TextField()

    foo = models.OneToOneField(
        Foo,
        related_name='multiple_foreign_key',
        on_delete=models.CASCADE,
    )
    bazz = models.OneToOneField(
        Bazz,
        related_name='multiple_foreign_key',
        on_delete=models.CASCADE,
    )

cache_relation(Foo.multiple_foreign_key)
cache_relation(Bazz.multiple_foreign_key)
