"""
Decorator utilities.
"""
import functools
import inspect

from taipan.functional import ensure_callable, or_


__all__ = ['decorator', 'function_decorator', 'class_decorator']


def decorator(decor):
    """Decorator for decorators (sic), written either as classes or functions.

    In either case, the decorator ``decor`` must be "doubly-callable":

        * for classes, this means implementing ``__call__`` method
          in addition to possible ``__init__``
        * for functions, this means returning a function that acts
          as an actual decorator, i.e. taking a function and returning
          its decorated version

    Although it works for any decorator, it's useful mainly for those
    that should take optional arguments. If the decorator is adorned
    with ``@function_decorator``, it's possible to use it without the pair of
    empty parentheses::

        @enhanced  # rather than @enhanced()
        def foo():
            pass

    when we don't want to pass any arguments to it.

    .. note::

        :func:`decorator` makes decorator appicable for both
        functions and classes. If you want to restrict the type of
        decorator targets, use either :func:`function_decorator`
        or :func:`class_decorator`.
    """
    ensure_callable(decor)
    return _wrap_decorator(decor, "functions or classes",
                           or_(inspect.isfunction, inspect.isclass))


def function_decorator(decor):
    """Decorator for function decorators (sic), written either
    as classes or functions.

    In either case, the decorator ``decor`` must be "doubly-callable":

        * for classes, this means implementing ``__call__`` method
          in addition to possible ``__init__``
        * for functions, this means returning a function that acts
          as an actual decorator, i.e. taking a function and returning
          its decorated version

    Although it works for any decorator, it's useful mainly for those
    that should take optional arguments. If the decorator is adorned
    with ``@function_decorator``, it's possible to use it without the pair of
    empty parentheses::

        @enhanced  # rather than @enhanced()
        def foo():
            pass

    when we don't want to pass any arguments to it.

    .. note::

        :func:`function_decorator` makes decorator applicable
        only to functions. Use :func:`decorator` or :func:`class_decorator`
        for decorators that should be applicable to classes.
    """
    ensure_callable(decor)
    return _wrap_decorator(decor, "functions", inspect.isfunction)


def class_decorator(decor):
    """Decorator for class decorators (sic), written either
    as classes or functions.

    In either case, the decorator ``decor`` must be "doubly-callable":

        * for classes, this means implementing ``__call__`` method
          in addition to possible ``__init__``
        * for functions, this means returning a function that acts
          as an actual decorator, i.e. taking a function and returning
          its decorated version

    Although it works for any decorator, it's useful mainly for those
    that should take optional arguments. If the decorator is adorned
    with ``@class_decorator``, it's possible to use it without the pair of
    empty parentheses::

        @enhanced  # rather than @enhanced()
        def foo():
            pass

    when we don't want to pass any arguments to it.

    .. note::

        :func:`class_decorator` makes decorator applicable only to classes.
        Use :func:`decorator` or :func:`class_decorator` for decorators
        that should be applicable to functions.
    """
    ensure_callable(decor)
    return _wrap_decorator(decor, "classes", inspect.isclass)


# Implementation

def _wrap_decorator(decorator, targets, is_valid_target):
    """Wraps given decorator in order to provide additional functionality:
    optional arguments and verification of decorator's target type.

    :param decorator: Decorator callable
    :param targets: Name of the decorator targets, as plural
                    (used in error messages)
    :param is_valid_target: Callable for checking
                            whether decorator's target is valid

    :return: Wrapped ``decorator``
    """
    @functools.wraps(decorator)
    def wrapper(*args, **kwargs):
        # handle the case when decorator is applied as ``@decorator``
        # (without any parameters and parentheses)
        one_arg = len(args) == 1 and not kwargs
        if one_arg and is_valid_target(args[0]):
            actual_decorator = decor()
            return actual_decorator(args[0])

        # pass the parameters to decorator callable
        # to get the actual decorator that can be applied to targets
        actual_decorator = decorator(*args, **kwargs)

        # wrap it inside a function that verifies
        # whether the target that user has given is valid for this decorator
        @functools.wraps(actual_decorator)
        def decorator_wrapper(target):
            if not is_valid_target(target):
                raise TypeError(
                    "@%s can only be applied to %s: got %r instead" % (
                        actual_decorator.__name__, targets, type(target)))
            return actual_decorator(target)

        return decorator_wrapper

    return wrapper
