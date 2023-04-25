import numpy as np
from cvxopt import matrix, solvers

def max_sharpe_ratio(mu, Sigma, r_f=0.2):
    # Define variables for optimization problem
    n = len(mu)
    ar = Sigma.values
    P = matrix(ar)
    q = matrix(np.zeros((n, 1)))
    G = matrix(np.concatenate((-mu.reshape(-1, 1), -np.eye(n)), axis=1))
    h = matrix(np.concatenate((np.array([-r_f]), np.zeros(n))))

    # Solve the optimization problem
    sol = solvers.qp(P, q, G, h)

    # Extract portfolio weights
    w = np.array(sol['x']).reshape(-1)

    return w
