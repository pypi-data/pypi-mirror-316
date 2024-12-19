from abc import ABC, abstractmethod
from fastapi import FastAPI


class A(ABC):
    factory_list = [C, B]
    app: FastAPI = None
    
    @abstractmethod
    def ex(self):
        pass

        
class AA(A):
    total_qian = 0
    
    def ex(self):
        pass
    
    def qian(self):
        for factory in self.factory_list:
            self.total_qian+=factory.qian()
        return self

class B(A):
    def ex(self):
        print("B ex")

    def __init__(self):
        self.factory_list.append(self)


    def __repr__(self):
        return "B"
    def qian(self):
        return 10


@dec
class C(A):
    def ex(self):
        print("algo")
        self.res = "algo"

        
    def __init__(self):
        self.factory_list.append(self)
        self.app = FastAPI()

    def __repr__(self):
        return "C"
    
    def qian(self):
        return self.res


if __name__ == "__main__":
    b = B()
    c = C()
    
    print(B.__mro__)    
    # ===============
    # print(globals())
    aa = AA()
    print(aa.app)
