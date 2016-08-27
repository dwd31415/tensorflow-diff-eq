import tensorflow as tf
import numpy as np

class DifferentialQuantity():
    def __init__(self,id,eq):
        self.id = id
        self.eq = eq
        self.is_defined = False
        self.derivatives = []

    def d(self,grade):
        if not self.is_defined:
            raise Exception("Quantity is not yet defined.")

        if grade < len(self.derivatives):
            raise Exception("Requested derivative not defined.")

        return self.derivatives[grade]

    def get_id(self):
        return self.id

    def define(self,derivatives):
        self.derivatives = derivatives
        self.is_defined = True

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

    def define_quantity(self,quantity,initial_value,initial_value_order,definition,definition_order):
        if not quantity.eq == self:
            raise Exception("The supplied quantity is not part of this differential equation.")

        if initial_value_order <= definition_order:
            raise Exception("The initial value has to be assigned to a higher derivative than is being defined.")
        derivatives = []
        for n in range(definition_order - 1):
            dx = None
            if n == initial_value_order:
                dx = tf.Variable(initial_value)
            else:
                dx = tf.Variable(np.zeros(np.size(initial_value)))
            derivatives.append(dx)
        derivatives.append(definition)

    def generate_simulate_operation(self,dt,step_size):
        # Are all quantities defined?
        for quantity in self.quantities:
            if not quantity.is_defined:
                raise Exception("All Quantities, which belong to this equation, must be defined in order for the simulate operation to be created.")

        updates = []
        for quantity in self.quantities:
            for n in range(len(quantity.derivatives)-1):
                updates.append(quantity.derivatives[n].assign(quantity.derivatives[n] + dt * (quantity.derivatives[n + 1])))
        return tf.group(updates)

                




