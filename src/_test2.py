

class A():
    def process(self, fn, c):
        fn()
        print("editing")
        c = 23


class B:
    def __init__(self, a) -> None:
        self.a = A()
        self.__c = 32

    def __pr(self):
        print(self.__c)

    def super_print(self):
        self.a.process(self.__pr, self.__c)

    @property
    def cc(self):
        return self.__c


b = B(A)
b._B__pr()
b.super_print()
print(b.cc)
