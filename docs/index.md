# Welcome to tensorflow-diff-eq
A python package for simulating differential equations using [TensorFlow](https://www.tensorflow.org/). 

![Lorenz Attractor](https://github.com/dwd31415/tensorflow-diff-eq/blob/master/examples/lorenz_attractor_animated.gif?raw=true)
## Why TensorFlow?
[TensorFlow](https://www.tensorflow.org/) is an open source library for numerical computation(mostly in machine learning), that allows one to specify computations using abstract dataflow graphs. The library then runs them on the GPU or CPU, this makes TensorFlow great for simulating differential equations. GPUs can perform many computation much faster than CPUs, using this library one can harness this performance for simulating differential equations. The simulation can run on the GPU or the CPU without any change in code.

## Installation
This package is still in an early stage of development, therefore it is not yet
available from PyPI. To install it, just clone this repository and run:

```
python3 setup.py install
```

## Basic Usage

This package allows you to symbolically define differential equation and
simulate them using TensorFlow, this allows one to use the GPU for the actual simulation without ever using C
or CUDA. All important classes and functions are in the `diff_eq` namespace, therefore
this is best way to import tensorflow-diff-eq:
``` python3
import tensorflow_diff_eq.diff_eq as diff_eq
```

The first step in defining a differential equation is to create a `DifferentialEquation`
object:
``` python3
eq = diff_eq.DifferentialEquation()
```
!!! warning
    Partial differential equations are currently not supported (but I am working on it and contributions are always welcome).

Then you must specify how many quantities will be involved in your differential equation.
### Example:
``` python3
(x, k, m) = eq.generate_quantities(3)
```
Once you have the references for these quantities you can define them using the
`define_quantity` function.
### Example:
``` python3
eq.define_quantity(k, 3.0, 0, 1)(0.0)
eq.define_quantity(m, 0.7, 0, 1)(0.0)
eq.define_quantity(x, 1.0, 1, 2)(-k.d(0)*x.d(0)/m.d(0))
```
The first argument to this function is the quantity which is being defined, the second parameter is an initial value and the third parameter is the grade of the derivative, that shall be
initialized with it. All other derivatives are initialized to zero of the respective datatype.
The forth argument is the grade of the "definition" derivative, this definition has the form
$$\frac{d^nx}{dt^n} = \phi,$$
where \(n\) is the grade supplied as the forth argument and \(\phi\) is any expression
involving previously defined quantities or \(x\), which is the quantity that is currently being defined. Arbitrary \(n^{th}\)-grade derivatives of the quantities are accessed using `.d(n)`, the quantity itself has to be accessed using `.d(0)`.

Once you have supplied the system with the differential equation in this fashion, you can start the simulation. In order to do this, you must generate a tensorflow operation that runs
the simulation. Such an operation can be generated using `eq.generate_simulate_operation` and can then be run using a tensorflow session. The function has one argument which is the \(\Delta t\) that will be used for the simulation.


!!! warning
    Please make sure you run the **tf.initialize_all_variables()** operation after defining the quantities involved in your differential equation.


###Example:
``` python3
# Start tensorflow
sess = tf.Session()
sess.run(tf.initialize_all_variables())
simulate_op = eq.generate_simulate_operation(0.005)
```

At this point you can just do `sess.run(simulate_op)` to simulate, if you want to access
any quantity at any time you can run `sess.run(x.d(0))`, where \(x\) is the quantity that you want to know the value of.

If you wish want to know more about how this package works, have a look at the example it the [examples folder](https://github.com/dwd31415/tensorflow-diff-eq/tree/master/examples).

!!! tip
    It is quite handy to define a *t* quantity and set it's first derivative to one in order to keep track of the "time". The library does not do this for you.
