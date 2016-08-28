import diff_eq
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

eq = diff_eq.DifferentialEquation()

# Define the quantities involved in the harmonic oscillator
(x, k, m) = eq.generate_quantities(3)

# Define these quantities
eq.define_quantity(k, 3.0, 0, 1)(0.0)
eq.define_quantity(m, 0.7, 0, 1)(0.0)

# The actual equation
eq.define_quantity(x, 1.0, 1, 2)(-k.d(0)*x.d(0)/m.d(0))

# Start tensorflow
sess = tf.Session()
sess.run(tf.initialize_all_variables())
simulate_op = eq.generate_simulate_operation(0.005)


# Simulate and record values
xs = np.zeros(2000)
ts = np.zeros(2000)
for i in range(2000):
    xs[i] = sess.run(x.d(0))
    if i < 1999:
        sess.run(simulate_op)
        sess.run(simulate_op)
        ts[i+1] = ts[i] + 0.01

plt.plot(ts,xs)
plt.show()
