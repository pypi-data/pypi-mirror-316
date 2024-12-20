from asyncio import ensure_future, iscoroutinefunction
from contextlib import suppress
from functools import cached_property, lru_cache, partial, wraps
from inspect import iscoroutine, isfunction, ismethod

from kalib.internals import (
    Nothing,
    Who,
    class_of,
    get_attr,
    get_owner,
    is_class,
    issubstance,
)

__all__ = 'Class', 'Property', 'cache', 'pin'


def cache(limit=None):

    function = partial(lru_cache, maxsize=None, typed=False)
    if isfunction(limit) or iscoroutine(limit) or ismethod(limit):
        return function()(limit)

    if limit is not None and (not isinstance(limit, float | int) or limit <= 0):
        msg = f'limit must be None or positive integer, not {Who.Is(limit)}'
        raise TypeError(msg)

    return function(maxsize=limit) if limit else function()


def call_descriptor(descriptor):
    if issubstance(descriptor, BaseProperty):
        return descriptor.call

    func = getattr(descriptor, 'fget', Nothing)
    if func is Nothing:
        head = f'expected descriptor derived from {Who(BaseProperty)}'

        if class_of(descriptor) is not cached_property:
            raise TypeError(f'{head}, but got {Who(descriptor)} instead')

        raise TypeError(
            f'{head}, but got {Who(descriptor)}, may be you use '
            f'@Property.Cached.Replace instead @Property.Cached?')

    return func


def parent_call(func):

    @wraps(func)
    def parent_caller(node, *args, **kw):
        try:
            desc = get_attr(
                class_of(node), func.__name__, exclude_self=True,
                index=bool(func.__name__ not in class_of(node).__dict__))
            return func(node, call_descriptor(desc)(node, *args, **kw), *args, **kw)

        except RecursionError as e:
            raise RecursionError(
                f'{Who(node)}.{func.__name__} call real {Who(func)}, '
                f"couldn't reach parent descriptor; "
                f"maybe {Who(func)} it's mixin of {Who(node)}?") from e

    return parent_caller


class PropertyError(Exception):
    ...


class InvalidContextError(PropertyError):
    ...


def invokation_context_check(func):

    @wraps(func)
    def context(self, node, *args, **kw):
        if (
            self.klass is not None and
            (node is None or self.klass != is_class(node))
        ):
            msg = (
                f'{Who(func)} exception, '
                f'{self.header_with_context(node)}, {node=}')

            if node is None and not self.klass:
                msg = f'{msg}; looks like as non-instance invokation'
            raise InvalidContextError(msg)

        return func(self, node, *args, **kw)
    return context


class BaseProperty:

    klass = False
    readonly = False

    def __init__(self, function):
        self.function = function

    @cached_property
    def name(self):
        return self.function.__name__

    @cached_property
    def is_data(self):
        return bool(hasattr(self, '__set__') or hasattr(self, '__delete__'))

    @cached_property
    def title(self):
        mode = 'mixed' if self.klass is None else ('instance', 'class')[self.klass]

        prefix = ('', 'data ')[self.is_data]
        return (
            f'{mode} {prefix}descriptor '
            f'{Who(self, addr=True)}'.strip())

    @cached_property
    def header(self):
        try:
            return f'{self.title}({self.function!a})'
        except Exception:  # noqa: BLE001
            return f'{self.title}({Who(self.function)})'

    def header_with_context(self, node):

        if node is None:
            mode = 'mixed' if self.klass is None else 'undefined'
        else:
            mode = ('instance', 'class')[is_class(node)]

        return f'{self.header} with {mode} ({Who(node, addr=True)}) call'

    @invokation_context_check
    def get_node(self, node):
        return node

    @invokation_context_check
    def call(self, node):
        value = self.function(node)
        return ensure_future(value) if iscoroutinefunction(self.function) else value

    def __str__(self):
        return f'<{self.header}>'

    def __repr__(self):
        return f'<{self.title}>'

    def __get__(self, instance, klass):
        if instance is None and self.klass is False:
            msg = f'{self.header_with_context(klass)}'
            raise InvalidContextError(msg)

        return self.call((instance, klass)[self.klass])


class Cached(BaseProperty):

    @invokation_context_check
    def get_cache(self, node):
        name = f'__{("instance", "class")[is_class(node)]}_memoized__'

        with suppress(KeyError):
            return node.__dict__[name]

        cache = {}
        setattr(node, name, cache)
        return cache

    @invokation_context_check
    def call(self, obj):
        node = self.get_node(obj)
        with suppress(KeyError):
            return self.get_cache(node)[self.name]
        return self.__set__(node, super().call(obj))

    @invokation_context_check
    def __set__(self, node, value):
        cache = self.get_cache(node)
        cache[self.name] = value
        return value

    @invokation_context_check
    def __delete__(self, node):
        cache = self.get_cache(node)
        with suppress(KeyError):
            del cache[self.name]


class ClassProperty(BaseProperty):
    klass = True

    @invokation_context_check
    def get_node(self, node):
        return get_owner(node, self.name) if is_class(node) else node


class MixedProperty(ClassProperty):
    klass = None

    def __get__(self, instance, klass):
        return self.call(instance or klass)


class ClassPin(ClassProperty, Cached): ...


class MixedPin(MixedProperty, Cached): ...


class Child(BaseProperty):

    @invokation_context_check
    def get_node(self, node):
        return node

    @classmethod
    def wrap(cls, klass):
        name = Who(klass, full=False)
        return type(
            f'{name}_child' if name == name.lower() else f'{name}Child',
            (cls, klass), {})


class Property(BaseProperty):

    Cached = Cached

    Mixed        = MixedProperty
    Mixed.Cached = Child.wrap(MixedPin)

    Root    = ClassPin
    Replace = cached_property


class Class:

    Property        = ClassProperty
    Property.Cached = Child.wrap(ClassPin)


class pin(Cached):  # noqa: N801

    # simple replace data-descriptor with calculated result
    attr = Property.Replace

    # class-descriptor, but .root uses class what have
    # declared pin.root, instead last child
    root = Property.Root
    cls  = Class.Property.Cached

    # mixed-descriptor, do not cache when using in class context, but bind instead
    any  = Property.Mixed.Cached
