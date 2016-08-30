import tensorflow_diff_eq.diff_eq as diff_eq
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import tqdm

eq = diff_eq.DifferentialEquation()

# Define the quantities,
(x,y,z) = eq.generate_quantities(3)
# and the parameters
sigma = 12.0
rho = 29.0
beta = 7.0/3.0

eq.prepare_quantity_for_recursive(x, 4.0, 0, 1)
eq.prepare_quantity_for_recursive(y, 2.0, 0, 1)
eq.prepare_quantity_for_recursive(z, 3.0, 0, 1)
# The Lorenz equations
eq.define_quantity_recursively(x, sigma * (y.d(0)-x.d(0)))
eq.define_quantity_recursively(y, x.d(0)*(rho - z.d(0))-y.d(0))
eq.define_quantity_recursively(z, x.d(0)*y.d(0) - z.d(0)*beta)

# Start tensorflow
sess = tf.Session()
sess.run(tf.initialize_all_variables())
simulate_op = eq.generate_simulate_operation(0.005)

N = 2000
xs = np.zeros(N)
ys = np.zeros(N)
zs = np.zeros(N)
ts = np.zeros(N)
(x,y,z) = (x.d(0),y.d(0),z.d(0))
for i in tqdm.tqdm(range(N)):
    xs[i] = sess.run(x)
    ys[i] = sess.run(y)
    zs[i] = sess.run(z)
    if i < N - 1:
        sess.run(simulate_op)
        sess.run(simulate_op)
        ts[i+1] = ts[i] + 0.01

np.save("lorenz_sim_data", [xs, ys, zs])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(xs, ys, zs)
ax.legend()

plt.show()