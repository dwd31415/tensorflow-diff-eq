# Optimizing your Simulations

## Vectors
To make your code perform better, try to pack as many quantities as possible into vectors. Especially on GPUs this dramatically 
increases the performance of your code. 
###Example (Three different scalar quantities):
``` python
(x,y,z) = eq.generate_quantities(3)
eq.prepare_quantity_for_recursive(x, 4.0, 0, 1)
eq.prepare_quantity_for_recursive(y, 2.0, 0, 1)
eq.prepare_quantity_for_recursive(z, 3.0, 0, 1)
eq.define_quantity_recursively(x, sigma * (y.d(0)-x.d(0)))
eq.define_quantity_recursively(y, x.d(0)*(rho - z.d(0))-y.d(0))
eq.define_quantity_recursively(z, x.d(0)*y.d(0) - z.d(0)*beta)
```
###Example (One vector quantity):
``` python
(xyz,) = eq.generate_quantities(1)
eq.define_quantity(xyz,np.array([2.1, 3.2, 4.4]), 0, 1)(tf.pack([sigma * (xyz.d(0)[1]-xyz.d(0)[0]),
                                                                    xyz.d(0)[0] * (rho - xyz.d(0)[2]) - xyz.d(0)[1],
                                                                    xyz.d(0)[0]*xyz.d(0)[1] - beta * xyz.d(0)[2]]))

```
You can see the performance increase for yourself by comparing the performance of the two Lorenz Attractor examples, 
the `lorenz_attractor_recursive.py` script uses three different quantities, while `lorenz_attractor.py` uses a vector quantity.