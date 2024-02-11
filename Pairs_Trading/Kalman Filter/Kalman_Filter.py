
import statsmodels.api as sm
import quantstats as qs
import numpy as np
from pykalman import KalmanFilter

class Kalman_Filter():

    def __init__(self, data_1, data_2) -> None:
        self.data_1 = data_1
        self.data_2 = data_2
        self.result = None

    def Backtest(self):
        self.data_1 = self.data_1.reindex(
            self.data_2.index, method='ffill')  # fill forward

        stock1 = self.data_1
        stock2 = self.data_2
        signal = self.data_1

        # calculate the spread
        signal['spread'] = stock1['Close'] - stock2['Close']

        signal['stock1_signal'] = 0
        signal['stock2_signal'] = 0

        # Create the Kalman filter object

        # Signal generation logic

        sigma = np.std(signal['spread'])

        # Define the long-term mean
        mu = np.mean(signal['spread'])

        # Define the transition matrix
        A = np.array([1])

        # Define the transition covariance
        Q = np.array([0.1])

        # Define the measurement matrix
        H = np.array([1])

        # Define the measurement covariance
        R = np.array([0.1])

        x = 0
        P = 1

        # Define the initial state
        x_init = np.array([mu])
        P_init = np.array([1])

        # Initialize the Kalman filter
        kf = KalmanFilter(transition_matrices=A, observation_matrices=H,
                          transition_covariance=Q, observation_covariance=R,
                          initial_state_mean=x_init, initial_state_covariance=P_init)

        # Loop over time steps
        for i in range(len(signal['spread'])):
            # Prediction
            x_pred, P_pred = kf.filter_update(
                filtered_state_mean=x, filtered_state_covariance=P)

            # Measurement
            z = signal['spread'][i]

            # Update
            x, P = kf.filter_update(filtered_state_mean=x_pred,
                                    filtered_state_covariance=P_pred, observation=z)

            (filtered_state_means, filtered_state_covariances) = kf.filter(
                signal['spread'][i])

        # Extract the final estimate of the spread
            estimated_spread = filtered_state_means[-1]
            # print(estimated_spread)

            # Extract the final estimate of the spread uncertainty
            estimated_spread_uncertainty = filtered_state_covariances[-1]
            # print(estimated_spread_uncertainty)

            # Signal generation logic

        #    estimated_spread_uncertainty > sigma
            if estimated_spread > mu:
                signal.loc[signal.index[i], 'stock1_signal'] = 1
                signal.loc[signal.index[i], 'stock2_signal'] = -1
            elif estimated_spread < mu:
                signal.loc[signal.index[i], 'stock1_signal'] = -1
                signal.loc[signal.index[i], 'stock2_signal'] = 1
            else:
                signal.loc[signal.index[i], [
                    'stock1_signal', 'stock2_signal']] = 0

        self.result = signal
        return signal

    def Run(self):

        self.Backtest()
        signal = self.result.copy()
        signal['returns'] = signal['Close'].pct_change()
        self.data_2['returns'] = self.data_2['Close'].pct_change()

        signal['returns2'] = self.data_2['returns']

        signal['returns_all'] = signal['returns'] * signal['stock1_signal'].shift(1) + \
            signal['returns2'] * signal['stock2_signal'].shift(1)

        return signal

    def Stat(self):
        self.data_1 = self.data_1.reindex(
            self.data_2.index, method='ffill')  # fill forward

        model = sm.OLS(self.data_1['Close'], self.data_2['Close'])
        result = model.fit()
        return result.summary()
