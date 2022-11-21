import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import arma_order_select_ic
import pmdarima as pm

def process(data: pd.DataFrame):
    print("Processing data")
    df = data.drop_duplicates(subset=['date'], keep='first')
    df = df.set_index('date')
    df = df['price']


    df = df.asfreq('D')
    df = df.resample('M').mean()


    #df = df.diff().dropna()
    #df = df.diff().dropna()
    tsplot(df, lags=10)
    plt.show()

    #order_select = arma_order_select_ic(df, ic='aic', trend='c')
    #print(order_select)
    #order = order_select['aic_min_order']
    stepwise_fit = pm.auto_arima(df, start_p=1, start_q=1,
                                 max_p=5, max_q=5, m=0,
                                 start_P=0, seasonal=False,
                                 d=0, trace=False,
                                 information_criterion='bic',
                                 stepwise=True)
    model = ARIMA(df, order=stepwise_fit.to_dict()['order'], trend='n')


    res = model.fit()
    preds = res.get_prediction(end='2022-12-31')
    ci = preds.conf_int()
    #fig = ci.plot(color='grey', figsize=(10, 5))
    fig = plt.figure()
    res.data.orig_endog.plot(label='data', marker='.', fig=fig)
    preds.predicted_mean.plot(label='predictions', fig=fig)
    plt.legend()
    plt.show()


def tsplot(y, lags=15):
    """
    Function to plot time series with ACF and PACF.
    Source: https://gitlab.fit.cvut.cz/dedeckam/mi-scr
    """

    if not isinstance(y, pd.Series):
        y = pd.Series(y)

    # layout
    fig = plt.figure(figsize=(14, 6))
    layout = (2, 2)
    ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
    acf_ax = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))

    # ts plot
    y.plot(ax=ts_ax)
    ts_ax.set_title('Time series');

    # acf, pacf
    plot_acf(y, lags=lags, ax=acf_ax, alpha=0.5)
    plot_pacf(y, lags=lags, ax=pacf_ax, alpha=0.5, method='ywm') 

