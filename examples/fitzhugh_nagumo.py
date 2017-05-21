import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import diff_eq as diff_eq


# xdot = c(xdot + ydot - (xdot**3/3) + i)
# ydot = -1/c(xdot - a + b*ydot)

# Where:     a = (0.75, a)[a is not None]
#            b = (0.8, b)[b is not None]
#            c = (3, c)[c is not None]
#            i = (-0.4, i)[i is not None]


eq = diff_eq.DifferentialEquation()

(xy,) = eq.generate_quantities(1)
# and the parameters
a = 0.75
b = 0.8
c = 3
i = -0.4

# The Fitzhugh-Nagumo equations
eq.define_quantity(xy, np.array([0.1, 0.1]), 0, 1)(tf.stack([c * (xy.d(0)[0] + xy.d(0)[1] - (xy.d(0)[0]**3/3) + i),
                                                            -1/c * (xy.d(0)[0] - a + b*xy.d(0)[1])]))


if __name__ == '__main__':
    # Start tensorflow
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())
    simulate_op = eq.generate_simulate_operation(0.025)

    xs = np.zeros(2000)
    ys = np.zeros(2000)
    ts = np.zeros(2000)
    (x, y) = (xy.d(0)[0], xy.d(0)[1])
    for i in tqdm.tqdm(range(2000)):
        xs[i] = sess.run(x)
        ys[i] = sess.run(y)
        if i < 1999:
            sess.run(simulate_op)
            sess.run(simulate_op)
            ts[i+1] = ts[i] + 0.01

    fig = plt.figure()
    plt.plot(ts, xs)
    plt.title('Fitzhugh-Nagumo Neuron')
    plt.legend()
    plt.show()