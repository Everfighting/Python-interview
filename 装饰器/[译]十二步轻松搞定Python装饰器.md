装饰器是一个很著名的设计模式，经常被用于有切面需求的场景，较为经典的有插入日志、性能测试、事务处理等。
装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量函数中与函数功能本身无关的雷同代码并继续重用。
概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。

- 函数

        >>> def foo():
        ...     return 1
        >>> foo()

- 作用域

        >>> a_string = "This is a global variable"
        >>> def foo():
        ...     print locals()
        >>> print globals()
        {..., 'a_string': 'This is a global variable'}
        >>> foo() # 2
        {}






- 变量解析规则

        >>> a_string = "This is a global variable"
        >>> def foo():
        ...     print a_string # 1
        >>> foo()
        This is a global variable

        >>> a_string = "This is a global variable"
        >>> def foo():
        ...     a_string = "test" # 1
        ...     print locals()
        >>> foo()
        {'a_string': 'test'}
        >>> a_string # 2
        'This is a global variable'

- 变量生存周期

        >>> def foo():
        ...     x = 1
        >>> foo()
        >>> print x # 1
        Traceback (most recent call last):
          ...
        NameError: name 'x' is not defined

- 函数参数

        >>> def foo(x):
        ...     print locals()
        >>> foo(1)
        {'x': 1}

        >>> def foo(x, y=0): # 1
        ...     return x - y
        >>> foo(3, 1) # 2
        2
        >>> foo(3) # 3
        3
        >>> foo() # 4
        Traceback (most recent call last):
          ...
        TypeError: foo() takes at least 1 argument (0 given)
        >>> foo(y=1, x=3) # 5
        2

- 嵌套函数

        >>> def outer():
        ...     x = 1
        ...     def inner():
        ...         print x # 1
        ...     inner() # 2
        ...
        >>> outer()
        1

- 函数是python世界里的一级类对象

        >>> issubclass(int, object) # all objects in Python inherit from a common baseclass
        True
        >>> def foo():
        ...     pass
        >>> foo.__class__ # 1
        <type 'function'>
        >>> issubclass(foo.__class__, object)
        True

        >>> def add(x, y):
        ...     return x + y
        >>> def sub(x, y):
        ...     return x - y
        >>> def apply(func, x, y): # 1
        ...     return func(x, y) # 2
        >>> apply(add, 2, 1) # 3
        3
        >>> apply(sub, 2, 1)
        1

        >>> def outer():
        ...     def inner():
        ...         print "Inside inner"
        ...     return inner # 1
        ...
        >>> foo = outer() #2
        >>> foo
        <function inner at 0x...>
        >>> foo()
        Inside inner

- 闭包

        >>> def outer():
        ...     x = 1
        ...     def inner():
        ...         print x # 1
        ...     return inner
        >>> foo = outer()
        >>> foo.func_closure
        (<cell at 0x...: int object at 0x...>,)

        >>> def outer(x):
        ...     def inner():
        ...         print x # 1
        ...     return inner
        >>> print1 = outer(1)
        >>> print2 = outer(2)
        >>> print1()
        1
        >>> print2()
        2

- 装饰器

        >>> def outer(some_func):
        ...     def inner():
        ...         print "before some_func"
        ...         ret = some_func() # 1
        ...         return ret + 1
        ...     return inner
        >>> def foo():
        ...     return 1
        >>> decorated = outer(foo) # 2
        >>> decorated()
        before some_func
        2

        >>> foo = outer(foo)
        >>> foo # doctest: +ELLIPSIS
        <function inner at 0x...>

        >>> class Coordinate(object):
        ...     def __init__(self, x, y):
        ...         self.x = x
        ...         self.y = y
        ...     def __repr__(self):
        ...         return "Coord: " + str(self.__dict__)
        >>> def add(a, b):
        ...     return Coordinate(a.x + b.x, a.y + b.y)
        >>> def sub(a, b):
        ...     return Coordinate(a.x - b.x, a.y - b.y)
        >>> one = Coordinate(100, 200)
        >>> two = Coordinate(300, 200)
        >>> add(one, two)
        Coord: {'y': 400, 'x': 400}

        >>> one = Coordinate(100, 200)
        >>> two = Coordinate(300, 200)
        >>> three = Coordinate(-100, -100)
        >>> sub(one, two)
        Coord: {'y': 0, 'x': -200}
        >>> add(one, three)
        Coord: {'y': 100, 'x': 0}

        >>> def wrapper(func):
        ...     def checker(a, b): # 1
        ...         if a.x < 0 or a.y < 0:
        ...             a = Coordinate(a.x if a.x > 0 else 0, a.y if a.y > 0 else 0)
        ...         if b.x < 0 or b.y < 0:
        ...             b = Coordinate(b.x if b.x > 0 else 0, b.y if b.y > 0 else 0)
        ...         ret = func(a, b)
        ...         if ret.x < 0 or ret.y < 0:
        ...             ret = Coordinate(ret.x if ret.x > 0 else 0, ret.y if ret.y > 0 else 0)
        ...         return ret
        ...     return checker
        >>> add = wrapper(add)
        >>> sub = wrapper(sub)
        >>> sub(one, two)
        Coord: {'y': 0, 'x': 0}
        >>> add(one, three)
        Coord: {'y': 200, 'x': 100}

- 使用@装饰符将装饰器应用到函数

        >>> @wrapper
        ... def add(a, b):
        ...     return Coordinate(a.x + b.x, a.y + b.y)

- *args 和 **kwargs

        >>> def one(*args):
        ...     print args # 1
        >>> one()
        ()
        >>> one(1, 2, 3)
        (1, 2, 3)
        >>> def two(x, y, *args): # 2
        ...     print x, y, args
        >>> two('a', 'b', 'c')
        a b ('c',)

        >>> def add(x, y):
        ...     return x + y
        >>> lst = [1,2]
        >>> add(lst[0], lst[1]) # 1
        3
        >>> add(*lst) # 2
        3

        >>> def foo(**kwargs):
        ...     print kwargs
        >>> foo()
        {}
        >>> foo(x=1, y=2)
        {'y': 2, 'x': 1}

        >>> dct = {'x': 1, 'y': 2}
        >>> def bar(x, y):
        ...     return x + y
        >>> bar(**dct)
        3


- 更通用的装饰器

        >>> def logger(func):
        ...     def inner(*args, **kwargs): #1
        ...         print "Arguments were: %s, %s" % (args, kwargs)
        ...         return func(*args, **kwargs) #2
        ...     return inner

        >>> @logger
        ... def foo1(x, y=1):
        ...     return x * y
        >>> @logger
        ... def foo2():
        ...     return 2
        >>> foo1(5, 4)
        Arguments were: (5, 4), {}
        20
        >>> foo1(1)
        Arguments were: (1,), {}
        1
        >>> foo2()
        Arguments were: (), {}
        2