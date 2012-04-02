import datetime
import unittest
from pyramid import testing

from zope.interface import Interface
from zope.interface import alsoProvides

class TestGetTextRepr(unittest.TestCase):
    def setUp(self):
        testing.cleanUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, object, default):
        from ..discriminators import get_textrepr
        return get_textrepr(object, default)

    def test_no_adapter(self):
        from ...interfaces import ICatalogable
        context = testing.DummyModel(__provides__=ICatalogable)
        context.title = 'title'
        context.description = 'description'
        textrepr = self._callFUT(context, None)
        self.assertEqual(textrepr, 'title ' * 10 + 'description')

class _TestGetDate(object):

    def test_not_set(self):
        context = testing.DummyModel()
        result = self._callFUT(context, None)
        self.assertEqual(result, None)

    def test_w_datetime(self):
        from ...util import coarse_datetime_repr
        context = testing.DummyModel()
        now = datetime.datetime.now()
        self._decorate(context, now)
        result = self._callFUT(context, None)
        self.assertEqual(result, coarse_datetime_repr(now))

    def test_w_date(self):
        from ...util import coarse_datetime_repr
        context = testing.DummyModel()
        today = datetime.date.today()
        self._decorate(context, today)
        result = self._callFUT(context, None)
        self.assertEqual(result, coarse_datetime_repr(today))

    def test_w_invalid_value(self):
        context = testing.DummyModel()
        self._decorate(context, 'notadatetime')
        result = self._callFUT(context, None)
        self.assertEqual(result, None)

class TestGetCreationDate(unittest.TestCase, _TestGetDate):
    def _callFUT(self, object, default):
        from ..discriminators import get_creation_date
        return get_creation_date(object, default)

    def _decorate(self, context, val):
        context.created = val

class TestGetModifiedDate(unittest.TestCase, _TestGetDate):
    def _callFUT(self, object, default):
        from ..discriminators import get_modified_date
        return get_modified_date(object, default)

    def _decorate(self, context, val):
        context.modified = val

class TestGetPath(unittest.TestCase):
    def _callFUT(self, object, default):
        from ..discriminators import get_path
        return get_path(object, default)

    def test_it(self):
        context = testing.DummyModel()
        result = self._callFUT(context, None)
        self.assertEqual(result, '/')

class TestGetInterfaces(unittest.TestCase):
    def _callFUT(self, object, default):
        from ..discriminators import get_interfaces
        return get_interfaces(object, default)

    def test_it(self):
        context = testing.DummyModel()
        class Dummy1(Interface):
            pass
        class Dummy2(Interface):
            pass
        alsoProvides(context, Dummy1)
        alsoProvides(context, Dummy2)
        result = self._callFUT(context, None)
        self.assertEqual(sorted(result), [Dummy1, Dummy2, Interface])

class TestGetContainment(unittest.TestCase):
    def test_it(self):
        from ..discriminators import get_containment
        class Dummy1(Interface):
            pass
        class Dummy2(Interface):
            pass
        root = testing.DummyModel()
        alsoProvides(root, Dummy1)
        context = testing.DummyModel()
        alsoProvides(context, Dummy2)
        root['foo'] = context
        result = get_containment(context, None)
        self.assertEqual(sorted(result), [Dummy1, Dummy2, Interface])

class TestGetName(unittest.TestCase):
    def _callFUT(self, object, default):
        from ..discriminators import get_name
        return get_name(object, default)

    def test_it(self):
        class Dummy:
            pass
        context = Dummy()
        result = self._callFUT(context, None)
        self.assertEqual(result, None)
        context.__name__= 'bar'
        result = self._callFUT(context, None)
        self.assertEqual(result, 'bar')

class TestGetTitle(unittest.TestCase):
    def _callFUT(self, object, default):
        from ..discriminators import get_title
        return get_title(object, default)

    def test_it(self):
        context = testing.DummyModel()
        result = self._callFUT(context, None)
        self.assertEqual(result, '')
        context.title = 'foo'
        result = self._callFUT(context, None)
        self.assertEqual(result, 'foo')

    def test_lowercase(self):
        context = testing.DummyModel()
        result = self._callFUT(context, None)
        self.assertEqual(result, '')
        context.title = 'FoobaR'
        result = self._callFUT(context, None)
        self.assertEqual(result, 'foobar')

class TestGetACL(unittest.TestCase):
    def _callFUT(self, object, default):
        from ..discriminators import get_acl
        return get_acl(object, default)

    def test_it(self):
        context = testing.DummyModel()
        result = self._callFUT(context, None)
        self.assertEqual(result, None)
        context.__acl__ = 'foo'
        result = self._callFUT(context, None)
        self.assertEqual(result, 'foo')

class TestGetAllowedToView(unittest.TestCase):
    def _callFUT(self, object, default):
        from ..discriminators import get_allowed_to_view
        return get_allowed_to_view(object, default)

    def test_it(self):
        context = testing.DummyModel()
        result = self._callFUT(context, None)
        self.assertEqual(result, ['system.Everyone'])
