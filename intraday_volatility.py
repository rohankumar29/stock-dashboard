import yfinance
import matplotlib.pyplot as plt
import statistics
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_packages(tickers):
    years = (datetime.now() - relativedelta(years = 30)).strftime("%Y-%m-%d")        
    data = yfinance.download(tickers, start = years, group_by = 'ticker')
    return data

def simulation(closed, dates):
    volatility = []
    for i in range(len(closed) - 2):
        if np.isnan(closed.iloc[i]):
            continue
        changed = (np.log(closed.iloc[i+1]/closed.iloc[i]))
        if changed == 1:
            continue
        volatility.append(changed)
    variance = statistics.variance(volatility)
    std_vol = statistics.stdev(volatility)
    mean = statistics.mean(volatility)
    drift = mean - variance/2
    starting_price = closed.iloc[len(closed) - 1]   
    df = pd.DataFrame(index = dates, columns = ['Price'])
    df['Price'][0] = starting_price
    for i in range(364):
        if (i - 5)%7 == 0 or (i - 6)%7 == 0:
            df['Price'][i+1] = df['Price'][i]
            continue
        random_float = np.random.uniform(low = 0.000001, high = 0.99999999)
        change = std_vol*statistics.NormalDist().inv_cdf(random_float)
        df['Price'][i + 1] = np.exp(drift + change)*df['Price'][i]
    return df['Price']

def portfolio(the_list, s, the_weights):
    stock_data = load_packages(the_list)
    dates = pd.date_range(datetime.now(), periods = 365)
    for x in range(s):
        main_portfolio = pd.DataFrame(index = dates, columns = the_list)
        total_portfolio = pd.DataFrame(index = dates, columns = ['Total'])
        total_portfolio['Total'].iloc[:] = 0
        for i in range(len(the_list)):
            stock_id = the_list[i]
            price_id = stock_data[stock_id]["Close"]
            main_portfolio[stock_id] =  simulation(price_id, dates)*the_weights[i]
            total_portfolio['Total'] = total_portfolio['Total'] + main_portfolio[stock_id]
        total_portfolio['Total'] = (total_portfolio['Total']/total_portfolio['Total'].iloc[0] - 1)*100
        plt.plot(dates, total_portfolio['Total'], label = ("Trail: " + str(x)))
    plt.show()







