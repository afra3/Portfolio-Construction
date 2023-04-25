import numpy as np
import pandas as pd
from scipy.optimize import minimize

def risk_parity_model(covariance_matrix, asset_names):
    """
    Computes the weights of a risk parity portfolio.

    Parameters:
    - covariance_matrix (np.ndarray or pd.DataFrame): A square matrix of asset returns covariances.
    - asset_names (list): A list of asset names, corresponding to the rows and columns of the covariance matrix.

    Returns:
    - weights (dict): A dictionary of asset weights, with asset names as keys and weights as values.
    """
    # Convert the covariance matrix to a numpy array if it's a DataFrame
    if isinstance(covariance_matrix, pd.DataFrame):
        covariance_matrix = covariance_matrix.values

    # Define the objective function for risk parity optimization
    def objective_function(weights, covariance_matrix):
        # Calculate the portfolio risk
        portfolio_risk = np.sqrt(weights @ covariance_matrix @ weights.T)

        # Calculate the contribution of each asset to the portfolio risk
        # Each element sums up the interactive
        MRC = covariance_matrix @ weights.T
        # Risk Contribution
        # Use element-wise multiplication
        RC = np.multiply(MRC,weights.T) / portfolio_risk 

        # Calculate the difference between the target and actual risk contributions
        risk_contribution_diff = RC - 1 / covariance_matrix.shape[0]

        # Calculate the sum of squared differences
        sum_of_squares = np.sum(np.square(risk_contribution_diff))

        return sum_of_squares

    
    
    def total_weight_constraint(x):
        return np.sum(x)-1.0

    def long_only_constraint(x):
        return x

    cons = ({'type': 'eq', 'fun': total_weight_constraint},
    {'type': 'ineq', 'fun': long_only_constraint})
    
    # Define the initial guess for the weights (equal weighting)
    n_assets = covariance_matrix.shape[0]
    initial_weights = np.array([1 / n_assets] * n_assets)

    # 不允许做空
    bounds = [(0, 1)] * n_assets

    # Optimize the objective function using scipy.optimize.minimize
    result = minimize(objective_function, initial_weights, args=(covariance_matrix,), bounds=bounds, method='SLSQP',constraints=cons)

    # Extract the optimized weights from the result
    weights = dict(zip(asset_names, result.x))

    #return weights
    return weights
