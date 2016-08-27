import tensorflow as tf

class DifferentialQuantity():
    def __init__(self,id,eq):
        self.id = id
        self.eq = eq

    def get_id(self):
        return self.id

class DifferentialEquation():
    def __init__(self):
        self.quantities = []

    def generate_quantities(self,N):
        new_quantities = []
        for i in range(N):
            x = DifferentialQuantity(len(self.quantities)+1,self)
            new_quantities.append(x)
            self.quantities.append(x)
        return new_quantities

