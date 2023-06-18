import intraday_volatility as vol


s = 10

#define relation - Y = x1*y1 + ... + xn*yn, where yn is the stock price and xn is the relative weight

#Load in all of the necessary information
the_list = ["T", "SNOW", "AAPL", "AMZN", "MSFT", "TSLA", "GOOGL", "NVDA", "WE"]
the_weights = [0.15, 0.2, 0.1, 0.15, 0.2, 0.5, 0.1, 0.34, 0.8]
print("Please type in the respective stocks you are interested in")
vol.portfolio(the_list, s, the_weights)





