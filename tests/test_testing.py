"""
Tests for the .testing module (yep).

.. note::

    Unlike other tests, these cannot use :class:`TestCase` from ``.testing``
    module, for the simple and obvious reason that it is among the very things
    that we're trying to test here!
"""
try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

import taipan.testing as __unit__


class _Assertion(TestCase):
    """Base class for test cases testing assert* methods."""

    class _DummyTestCase(__unit__.TestCase):
        """"Dummy object of the tested :class:`TestCase`.
        It is required to invoke assertion methods that we want to test.
        """
        def runTest(self):
            pass

    _TESTCASE = _DummyTestCase()
    _FAILURE = _TESTCASE.failureException


class AssertStartsWith(_Assertion):
    PREFIX = "foo"
    STRING = "foobar"

    def test_prefix__none(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertStartsWith(None, self.STRING)

    def test_prefix__some_object(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertStartsWith(object(), self.STRING)

    def test_prefix__empty_string(self):
        self._TESTCASE.assertStartsWith("", self.STRING)

    def test_string__none(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertStartsWith(self.PREFIX, None)

    def test_string__some_object(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertStartsWith(self.PREFIX, object())

    def test_string__empty_string(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertStartsWith(self.PREFIX, "")

    def test_success(self):
        self._TESTCASE.assertStartsWith(self.PREFIX, self.STRING)


class AssertEndsWith(_Assertion):
    SUFFIX = "bar"
    STRING = "foobar"

    def test_suffix__none(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertEndsWith(None, self.STRING)

    def test_suffix__some_object(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertEndsWith(object(), self.STRING)

    def test_suffix__empty_string(self):
        self._TESTCASE.assertEndsWith("", self.STRING)

    def test_string__none(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertEndsWith(self.SUFFIX, None)

    def test_string__some_object(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertEndsWith(self.SUFFIX, object())

    def test_string__empty_string(self):
        with self.assertRaises(self._FAILURE):
            self._TESTCASE.assertEndsWith(self.SUFFIX, "")

    def test_success(self):
        self._TESTCASE.assertEndsWith(self.SUFFIX, self.STRING)