from unittest import mock

from django.core.cache import cache
from django.test import TestCase

from .models import Foo, Bazz, Quox


class CachedRelationForwardsTest(TestCase):
    longMessage = True

    def setUp(self):
        # Ensure we start with a clear cache for each test, i.e. tests can use
        # the cache hygenically
        cache.clear()

    def test_cached_relation(self):
        foo = Foo.objects.create(bar='bees')

        Bazz.objects.create(foo=foo, value=10)

        # Populate the cache
        Bazz.objects.get(foo_id=foo.pk).foo_cache

        # Get from the cache
        cached_object = Bazz.objects.get(foo_id=foo.pk).foo_cache

        self.assertEqual('bees', cached_object.bar)

    def test_cached_relation_none(self):
        quox = Quox.objects.create(val=10)

        self.assertIsNone(
            quox.foo_cache,
            "Quox should have None 'foo_cache' (empty cache)",
        )

        self.assertIsNone(
            quox.foo_cache,
            "Quox should have None 'foo_cache' (warm cache; before natural access)",
        )

        # sanity check
        self.assertIsNone(
            quox.foo,
            "Quox should have None 'foo' attribute",
        )

        self.assertIsNone(
            quox.foo_cache,
            "Quox should have None 'foo_cache' (warm cache; after natural access)",
        )

    def test_cached_relation_not_present_exception(self):
        quox = Quox.objects.create(val=10)
        quox.foo_id = 42

        with self.assertRaises(
            Foo.DoesNotExist,
            msg="Cache should fail to find object which does not exist (empty cache)",
        ):
            quox.foo_cache

        with self.assertRaises(
            Foo.DoesNotExist,
            msg="Cache should fail to find object which does not exist (warm cache; before natural access)",
        ), self.assertNumQueries(0):
            quox.foo_cache

        with self.assertRaises(
            Foo.DoesNotExist,
            msg="Natural lookup should fail to find object which does not exist",
        ):
            quox.foo

        with self.assertRaises(
            Foo.DoesNotExist,
            msg="Cache should fail to find object which does not exist (warm cache; after natural access)",
        ), self.assertNumQueries(0):
            quox.foo_cache

    def test_uses_select_related(self):
        foo = Foo.objects.create(bar='bees')
        Bazz.objects.create(foo=foo, value=10)

        with self.assertNumQueries(1):
            bazz = Bazz.objects.select_related('foo').get(foo_id=foo.pk)

        with self.assertNumQueries(0):
            self.assertEqual(foo, bazz.foo_cache)

    def test_get_instance_error_doesnt_have_side_effect_issues(self):
        foo = Foo.objects.create(bar='bees')
        Bazz.objects.create(foo=foo, value=10)
        bazz = Bazz.objects.get(foo_id=foo.pk)

        class DummyException(Exception):
            pass

        # Validate that the underlying error is passed through, without any
        # other errors happening...
        with mock.patch('cache_toolbox.core.cache.get', side_effect=DummyException):
            with self.assertRaises(DummyException):
                bazz.foo_cache

        # ... and that we haven't put anything bad in the cache along the way
        self.assertEqual(foo, bazz.foo_cache)
