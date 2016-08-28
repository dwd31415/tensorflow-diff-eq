import tensorflow_diff_eq.diff_eq as diff_eq
import tensorflow as tf
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import tqdm

eq = diff_eq.DifferentialEquation()

# Define the quantities,
(xyz,) = eq.generate_quantities(1)
# and the parameters
sigma = 10.0
rho = 28.0
beta = 8.0/3.0

# The Lorenz equations
eq.define_quantity(xyz,np.array([2.1, 3.2, 4.4]), 0, 1)(tf.pack([sigma * (xyz.d(0)[1]-xyz.d(0)[0]),
                                                                    xyz.d(0)[0] * (rho - xyz.d(0)[2]) - xyz.d(0)[1],
                                                                    xyz.d(0)[0]*xyz.d(0)[1] - beta * xyz.d(0)[2]]))

# Start tensorflow
sess = tf.Session()
sess.run(tf.initialize_all_variables())
simulate_op = eq.generate_simulate_operation(0.005,0)

xs = np.zeros(2000)
ys = np.zeros(2000)
zs = np.zeros(2000)
ts = np.zeros(2000)
(x,y,z) = (xyz.d(0)[0],xyz.d(0)[1],xyz.d(0)[2])
for i in tqdm.tqdm(range(2000)):
    xs[i] = sess.run(x)
    ys[i] = sess.run(y)
    zs[i] = sess.run(z)
    if i < 1999:
        sess.run(simulate_op)
        sess.run(simulate_op)
        ts[i+1] = ts[i] + 0.01

np.save("lorenz_sim_data", [xs, ys, zs])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(xs, ys, zs)
ax.legend()

plt.show()