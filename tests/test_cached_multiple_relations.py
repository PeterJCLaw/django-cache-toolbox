
from django.core.cache import cache
from django.test import TestCase

from .models import Foo, Bazz, MultipleForeignKey

class CachedRelationTest(TestCase):
    longMessage = True

    def setUp(self):
        # Ensure we start with a clear cache for each test, i.e. tests can use
        # the cache hygenically
        cache.clear()

    def test_cached_relations(self):
        foo = Foo.objects.create(bar='bees')
        bazz = Bazz.objects.create(foo=foo, value=10)

        MultipleForeignKey.objects.create(
            name='item',
            foo=foo,
            bazz=bazz,
        )

        # Populate the cache
        foo.multiple_foreign_key_cache
        bazz.multiple_foreign_key_cache

        # Get from the cache
        cached_from_foo = Foo.objects.get(pk=foo.pk).multiple_foreign_key_cache
        self.assertEqual('item', cached_from_foo.name)

        cached_from_bazz = Bazz.objects.get(pk=bazz.pk).multiple_foreign_key_cache
        self.assertEqual('item', cached_from_bazz.name)

    def test_cached_inverted_relations(self):
        foo_first = Foo.objects.create(pk=1, bar='foo-first')
        bazz_first = Bazz.objects.create(pk=1, foo=foo_first, value=10)
        foo_second = Foo.objects.create(pk=2, bar='foo-second')
        bazz_second = Bazz.objects.create(pk=2, foo=foo_second, value=20)

        MultipleForeignKey.objects.create(
            name='first',
            foo=foo_first,
            bazz=bazz_second,
        )
        MultipleForeignKey.objects.create(
            name='second',
            foo=foo_second,
            bazz=bazz_first,
        )

        # Populate the cache
        foo_first.multiple_foreign_key_cache
        bazz_first.multiple_foreign_key_cache
        foo_second.multiple_foreign_key_cache
        bazz_second.multiple_foreign_key_cache

        # Get from the cache
        cached_from_foo_first = Foo.objects.get(pk=1).multiple_foreign_key_cache
        self.assertEqual('first', cached_from_foo_first.name)

        cached_from_bazz_first = Bazz.objects.get(pk=1).multiple_foreign_key_cache
        self.assertEqual('second', cached_from_bazz_first.name)

        cached_from_foo_second = Foo.objects.get(pk=2).multiple_foreign_key_cache
        self.assertEqual('second', cached_from_foo_second.name)

        cached_from_bazz_second = Bazz.objects.get(pk=2).multiple_foreign_key_cache
        self.assertEqual('first', cached_from_bazz_second.name)
