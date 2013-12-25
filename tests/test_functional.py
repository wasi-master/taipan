"""
Tests for the .functional module.
"""
from taipan.testing import TestCase

import taipan.functional as __unit__


class EnsureCallable(TestCase):

    def test_none(self):
        with self.assertRaises(TypeError):
            __unit__.ensure_callable(None)

    def test_some_object(self):
        with self.assertRaises(TypeError):
            __unit__.ensure_callable(object())

    def test_number(self):
        with self.assertRaises(TypeError):
            __unit__.ensure_callable(42)

    def test_string(self):
        with self.assertRaises(TypeError):
            __unit__.ensure_callable("foo")

    def test_few_builtins(self):
        __unit__.ensure_callable(open)
        __unit__.ensure_callable(min)
        __unit__.ensure_callable(sum)
        __unit__.ensure_callable(str.__add__)

    def test_lambda(self):
        func = lambda : self.fail("lambda must not be acually called")
        __unit__.ensure_callable(func)

    def test_function(self):
        def func():
            self.fail("function must not be actually called")
        __unit__.ensure_callable(func)

    def test_class(self):
        class Foo(object):
            def __init__(self_):
                self.fail("class must not be actually instantiated")
        __unit__.ensure_callable(Foo)

    def test_callable_object(self):
        class Foo(object):
            def __call__(self_):
                self.fail("object must not be actually called")
        __unit__.ensure_callable(Foo())


class EnsureArgcount(TestCase):
    FEW_ARGS = ["foo", 'bar']
    MANY_ARGS = ["foo", 'bar', 1.41, False, None, (1,)]

    FEW = len(FEW_ARGS)
    MANY = len(MANY_ARGS)
    MORE_THAN_FEW = FEW + 1
    LESS_THAN_MANY = MANY - 1

    def test_no_limits(self):
        with self.assertRaises(ValueError):
            __unit__.ensure_argcount(self.FEW_ARGS)

    def test_invalid_limits(self):
        with self.assertRaises(ValueError) as r:
            __unit__.ensure_argcount(self.FEW_ARGS, min_=2, max_=1)
        self.assertIn("greater", str(r.exception))

    def test_args__none(self):
        with self.assertRaises(TypeError):
            __unit__.ensure_argcount(None, min_=1, max_=1)

    def test_args__some_object(self):
        with self.assertRaises(TypeError):
            __unit__.ensure_argcount(object(), min_=1, max_=1)

    def test_args__empty(self):
        __unit__.ensure_argcount([], min_=0, max_=0)
        __unit__.ensure_argcount([], min_=0, max_=self.MANY)
        with self.assertRaises(TypeError):
            __unit__.ensure_argcount([], min_=self.FEW)

    def test_args__less_than_min(self):
        with self.assertRaises(TypeError) as r:
            __unit__.ensure_argcount(self.FEW_ARGS, min_=self.MORE_THAN_FEW)
        self.assertIn("expected at least", str(r.exception))

    def test_args__more_than_max(self):
        with self.assertRaises(TypeError) as r:
            __unit__.ensure_argcount(self.MANY_ARGS, max_=self.LESS_THAN_MANY)
        self.assertIn("expected at most", str(r.exception))

    def test_args__exactly_min(self):
        __unit__.ensure_argcount(self.FEW_ARGS,
                                 min_=self.FEW, max_=self.MORE_THAN_FEW)

    def test_args__exactly_max(self):
        __unit__.ensure_argcount(self.MANY_ARGS,
                                 min_=self.LESS_THAN_MANY, max_=self.MANY)

    def test_args__exact(self):
        __unit__.ensure_argcount(self.FEW_ARGS, min_=self.FEW, max_=self.FEW)
        __unit__.ensure_argcount(self.MANY_ARGS, min_=self.MANY, max_=self.MANY)


# Constant functions

class Identity(TestCase):
    EMPTY_TUPLE = ()

    EMPTY_LIST = []
    DIFFERENT_EMPTY_LIST = []
    LIST = list(range(5))
    LIST_COPY = list(LIST)

    EMPTY_DICT = {}
    DIFFERENT_EMPTY_DICT = {}
    DICT = dict(zip('abcde', range(5)))
    DICT_COPY = dict(DICT)

    OBJECT = object()
    DIFFERENT_OBJECT = object()

    def test_values(self):
        identity = __unit__.identity()
        self.assertIsNone(identity(None))
        self.assertIs(0, identity(0))
        self.assertIs(self.EMPTY_TUPLE, identity(self.EMPTY_TUPLE))

    def test_empty_lists(self):
        identity = __unit__.identity()
        self.assertIs(self.EMPTY_LIST, identity(self.EMPTY_LIST))
        self.assertIsNot(self.DIFFERENT_EMPTY_LIST, identity(self.EMPTY_LIST))

    def test_lists(self):
        identity = __unit__.identity()
        self.assertIs(self.LIST, identity(self.LIST))
        self.assertIsNot(self.LIST_COPY, identity(self.LIST))

    def test_empty_dicts(self):
        identity = __unit__.identity()
        self.assertIs(self.EMPTY_DICT, identity(self.EMPTY_DICT))
        self.assertIsNot(self.DIFFERENT_EMPTY_DICT, identity(self.EMPTY_DICT))

    def test_dicts(self):
        identity = __unit__.identity()
        self.assertIs(self.DICT, identity(self.DICT))
        self.assertIsNot(self.DICT_COPY, identity(self.DICT))

    def test_object(self):
        identity = __unit__.identity()
        self.assertIs(self.OBJECT, identity(self.OBJECT))
        self.assertIsNot(self.DIFFERENT_OBJECT, identity(self.OBJECT))


class Const(TestCase):
    pass


class Compose(TestCase):
    pass


class LogicalCombinators(TestCase):
    pass
