import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel

import preprocess as pp

stime = time.time()

class GPModel:

    def __init__(self):
        #Matern kernel parameters are in order - amplitude, lengthscale, roughness
        #Choosing roughness (nu) as 1.5 means we assume that our ML function is differentiable at most once
        m_ker = Matern(length_scale = 1, length_scale_bounds = (1e-1, 1e3), nu = 1.5)
        #This kernel modifies the mean of the Gaussian process
        c_ker = ConstantKernel()
        #This kernel is used to explain the noise present in the data
        w_ker = WhiteKernel(noise_level = 1)
        self.kernel = m_ker + c_ker + w_ker

        #Pass our kernel to the GP Regressor and set the number of times we re-run
        #the optimizer in computing the hyperparameters
        self.gpr = GaussianProcessRegressor(kernel = self.kernel, n_restarts_optimizer = 10)

    def train(self, dataset_size=None, pred_size=None, data=None):
        #Our training data - energy consumption E at time T
        # T_tr = [[0], [1], [2], [3], [4], [5]]
        # E_tr = [5, 6, 7, 8, 9, 10]
        self.dataset_size = dataset_size
        self.pred_size = pred_size if pred_size else int(0.1 * dataset_size)

        T, E = pp.create_all_agg_demands()
        if self.dataset_size:
            T = T[:self.dataset_size]
            E = E[:self.dataset_size]

        if data:
            start, limit = T[-1], (T[-1] + self.pred_size * 1800)
            T_tr = T
            T_pred = [[d, id] for id, d in zip(data, range(start, limit, 1800))]
        else:
            T_tr, T_pred = T[:-(self.pred_size)], T[-(self.pred_size):]
                                                                                                                                                                   1,23          Top
