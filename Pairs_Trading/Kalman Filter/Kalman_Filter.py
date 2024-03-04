import statsmodels.api as sm
import quantstats as qs
import numpy as np
from pykalman import KalmanFilter
import pandas as pd


class Kalman_Filter():

    def __init__(self, data_1, data_2) -> None:
        self.data_1 = data_1
        self.data_2 = data_2
        self.results = None
        self.tp_year = None

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

    def Run(self, size=1 , ptc = 0.2 ,cash = 10000 , currency = None) :

        # magin = 1/100
        # size 1 = 0.01 lot
        # fix size

        #         ต้นทุนสเปรด
        # 0.20 USD
        # ค่าธรรมเนียม
        # 0 USD
        # สว็อปสั้น
        # 0 USD
        # สว็อปยาว
        # −0.33 USD
        # มูลค่าต่อปิ๊ป
        # 0.010000 USD

        tc = ptc * size

        
        if currency == None :
            pip = 1000
        elif currency == 'JPY' :
            pip = 6



        self.Backtest()
        signal = self.result.copy()
        signal['returns'] = signal['Close'].pct_change()
        self.data_2['returns'] = self.data_2['Close'].pct_change()
        self.data_2['Pnl_2'] = self.data_2['Close'] - self.data_2['Close'].shift(1)
        
        signal['Pnl_1'] = signal['Close'] - signal['Close'].shift(1)

        signal['returns2'] = self.data_2['returns']
        signal['Pnl_2'] = self.data_2['Pnl_2']

        signal.fillna(0, inplace=True)

        signal['Pnl'] = (signal['Pnl_1'] * signal['stock1_signal'].shift(1) +
                         signal['Pnl_2'] * pip * signal['stock2_signal'].shift(1)) * size
 
        signal['returns_all'] = (signal['returns'] * signal['stock1_signal'].shift(1) +
                                 signal['returns2'] * signal['stock2_signal'].shift(1)) * size
        
        signal.fillna(0, inplace=True)
        
        signal['check_tc'] = np.where(signal['stock1_signal'].shift(1) == signal['stock1_signal'], 0, 1)

        signal['returns_all'] = signal['returns_all'] - tc * signal['check_tc']

        signal['Pnl'] = signal['Pnl'] - tc * signal['check_tc']

       

        signal.fillna(0, inplace=True)

        signal['Equity'] = cash + tc + signal['Pnl'].cumsum()

        signal['Returns'] = signal['Equity'].pct_change().fillna(0)

        signal['strategy'] = signal['Equity'].pct_change().fillna(0)

        self.results = signal

        return signal

    def Stat(self):
        self.data_1 = self.data_1.reindex(
            self.data_2.index, method='ffill')  # fill forward

        model = sm.OLS(self.data_1['Close'], self.data_2['Close'])
        result = model.fit()
        return result.summary()

    ############################## Performance ######################################

    def print_performance(self, leverage=False):
        ''' Calculates and prints various Performance Metrics.
        '''

        self.data = self.data_1
        self.tp_year = (self.data.Close.count(
        ) / ((self.data.index[-1] - self.data.index[0]).days / 365.25))

        data = self.results.copy()

        if leverage:
            to_analyze = np.log(data.strategy_levered.add(1))
        else:
            to_analyze = data.strategy

        strategy_multiple = round(self.calculate_multiple(to_analyze), 6)
        bh_multiple = round(self.calculate_multiple(data.returns), 6)
        outperf = round(strategy_multiple - bh_multiple, 6)
        cagr = round(self.calculate_cagr(to_analyze), 6)
        ann_mean = round(self.calculate_annualized_mean(to_analyze), 6)
        ann_std = round(self.calculate_annualized_std(to_analyze), 6)
        sharpe = round(self.calculate_sharpe(to_analyze), 6)
        sortino = round(self.calculate_sortino(to_analyze), 6)
        max_drawdown = round(self.calculate_max_drawdown(to_analyze), 6)
        calmar = round(self.calculate_calmar(to_analyze), 6)
        max_dd_duration = round(self.calculate_max_dd_duration(to_analyze), 6)
        kelly_criterion = round(self.calculate_kelly_criterion(to_analyze), 6)

        print(100 * "=")
        # print("SIMPLE CONTRARIAN STRATEGY | INSTRUMENT = {} | Freq: {} | WINDOW = {}".format(
        #     self.symbol, self.freq, self.window))
        print(100 * "-")
        # print("\n")
        print("PERFORMANCE MEASURES:")
        print("\n")
        print("Multiple (Strategy):         {}".format(strategy_multiple))
        print("Multiple (Buy-and-Hold):     {}".format(bh_multiple))
        print(38 * "-")
        print("Out-/Underperformance:       {}".format(outperf))
        print("\n")
        print("CAGR:                        {}".format(cagr))
        print("Annualized Mean:             {}".format(ann_mean))
        print("Annualized Std:              {}".format(ann_std))
        print("Sharpe Ratio:                {}".format(sharpe))
        print("Sortino Ratio:               {}".format(sortino))
        print("Maximum Drawdown:            {}".format(max_drawdown))
        print("Calmar Ratio:                {}".format(calmar))
        print("Max Drawdown Duration:       {} Days".format(max_dd_duration))
        print("Kelly Criterion:             {}".format(kelly_criterion))

        print(100 * "=")

    def calculate_multiple(self, series):
        return np.exp(series.sum())

    def calculate_cagr(self, series):
        return np.exp(series.sum())**(1/((series.index[-1] - series.index[0]).days / 365.25)) - 1

    def calculate_annualized_mean(self, series):
        return series.mean() * self.tp_year

    def calculate_annualized_std(self, series):
        return series.std() * np.sqrt(self.tp_year)

    def calculate_sharpe(self, series):
        if series.std() == 0:
            return np.nan
        else:
            return series.mean() / series.std() * np.sqrt(self.tp_year)

    def calculate_sortino(self, series):
        excess_returns = (series - 0)
        downside_deviation = np.sqrt(
            np.mean(np.where(excess_returns < 0, excess_returns, 0)**2))
        if downside_deviation == 0:
            return np.nan
        else:
            sortino = (series.mean() - 0) / \
                downside_deviation * np.sqrt(self.tp_year)
            return sortino

    def calculate_max_drawdown(self, series):
        creturns = series.cumsum().apply(np.exp)
        cummax = creturns.cummax()
        drawdown = (cummax - creturns)/cummax
        max_dd = drawdown.max()
        return max_dd

    def calculate_calmar(self, series):
        max_dd = self.calculate_max_drawdown(series)
        if max_dd == 0:
            return np.nan
        else:
            cagr = self.calculate_cagr(series)
            calmar = cagr / max_dd
            return calmar

    def calculate_max_dd_duration(self, series):
        creturns = series.cumsum().apply(np.exp)
        cummax = creturns.cummax()
        drawdown = (cummax - creturns)/cummax

        begin = drawdown[drawdown == 0].index
        end = begin[1:]
        end = end.append(pd.DatetimeIndex([drawdown.index[-1]]))
        periods = end - begin
        max_ddd = periods.max()
        return max_ddd.days

    def calculate_kelly_criterion(self, series):
        series = np.exp(series) - 1
        if series.var() == 0:
            return np.nan
        else:
            return series.mean() / series.var()

    ############################## Performance ######################################
