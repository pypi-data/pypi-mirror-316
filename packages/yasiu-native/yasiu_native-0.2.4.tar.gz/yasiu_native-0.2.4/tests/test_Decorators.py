import pytest

from yasiu_native.decorators import flexible_decorator, flexible_decorator_2d


def testDecorOneLevel_1():

    @flexible_decorator
    def decor1(fun):
        def wrapper(*a, **kw):
            return fun(*a, **kw)
        return wrapper

    @decor1
    def funTest():
        pass
    funTest()


def testDecorOneLevel_2():

    @flexible_decorator
    def decor1(fun):
        def wrapper(*a, **kw):
            return fun(*a, **kw)
        return wrapper

    @decor1()
    def funTest():
        pass
    funTest()


def testDecorOneLevel_3():

    @flexible_decorator
    def decor1(fun, a=2):
        def wrapper(*a, **kw):
            return fun(*a, **kw)
        assert a == 5, "True"
        return wrapper

    @decor1(5)
    def funTest():
        pass
    funTest()


def testDecorOneLevel_4():

    @flexible_decorator
    def decor1(fun, a, b, g):
        def wrapper(*a, **kw):
            return fun(*a, **kw)
        return wrapper

    @decor1(2, 3, g=10)
    def funTest():
        pass
    funTest()


def testDecorOneLevel_5():
    "Test of decoration with function"

    @flexible_decorator
    def decor1(fun, callThis, a, b, g):
        def wrapper(*a, **kw):
            callThis(a, b)
            return fun(*a, **kw)
        return wrapper

    @decor1(sum, 2, 3, g=10)
    def funTest():
        pass
    funTest()


def testDecorOneLevel_6():
    "Test class decorators"

    @flexible_decorator
    def decor1(fun):
        def wrapper(*a, **kw):
            return fun(*a, **kw)
        return wrapper

    class TClass:
        @decor1
        def prt(self):
            pass

        @decor1
        @staticmethod
        def prtST(cls):
            pass

    ob = TClass()
    ob.prt()

    TClass.prtST


def testDecorOneLevel_7():
    "Test class decorators"

    @flexible_decorator
    def decor1(fun, param1=3):

        assert param1 == 5, "True"

        def wrapper(*a, **kw):
            return fun(*a, **kw)
        return wrapper

    class TClass:
        @decor1(5)
        def prt(self):
            pass

        @decor1(5)
        @staticmethod
        def prtST(cls):
            pass

    ob = TClass()
    ob.prt()

    TClass.prtST


# def testDecorOneLevel_8():
#     "Test of decoration with function"

#     @flexible_decorator
#     def decor1(fun, callThis):
#         def wrapper(*a, **kw):
#             print(f"Call this: {callThis}")
#             # callThis(1, 2)
#             return fun(*a, **kw)
#         return wrapper

#     @decor1(sum)
#     def funTest():
#         pass
#     funTest()


"""

=== Two Level Test ===

"""


def testDecorTwoLevel_1():

    @flexible_decorator_2d
    def decor2():
        def wrapper(fun):
            def inner(*a, **kw):
                return fun(*a, **kw)
            return inner
        return wrapper

    @decor2
    def testFun():
        pass

    testFun()

    @decor2
    def testFun(a=2):
        pass

    testFun()


def testDecorTwoLevel_2():

    @flexible_decorator_2d
    def decor2():
        def wrapper(fun):
            def inner(*a, **kw):
                return fun(*a, **kw)
            return inner
        return wrapper

    @decor2()
    def testFun():
        pass

    testFun()


def testDecorTwoLevel_3():

    @flexible_decorator_2d
    def decor2(param=2):

        assert param == 5, "True"

        def wrapper(fun):
            def inner(*a, **kw):
                return fun(*a, **kw)
            return inner
        return wrapper

    @decor2(param=5)
    def testFun():
        pass

    testFun()

    @decor2(5)
    def testFun():
        pass


def testDecorTwoLevel_3():

    @flexible_decorator_2d
    def decor2(param=2):

        assert param == 5, "True"

        def wrapper(fun):
            def inner(*a, **kw):
                return fun(*a, **kw)
            return inner
        return wrapper

    @decor2(param=5)
    def testFun():
        pass

    testFun()

    @decor2(5)
    def testFun():
        pass

    testFun()
    testFun()
