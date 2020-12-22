from cache_toolbox import cache_model, cache_relation

from django.db import models

class Foo(models.Model):
    bar = models.TextField()

class Bazz(models.Model):
    foo = models.OneToOneField(
        Foo,
        related_name='bazz',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    value = models.IntegerField(null=True)

class Quox(models.Model):
    foo = models.OneToOneField(
        Foo,
        related_name='quox',
        on_delete=models.CASCADE,
        null=True,
    )

    val = models.IntegerField(null=True)

cache_model(Foo)
cache_relation(Foo.bazz)
cache_relation(Bazz.foo)
cache_relation(Quox.foo)
