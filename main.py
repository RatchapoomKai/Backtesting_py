from backtesting import Backtest
from data_loader import load_data
from strategy_sma import SmaCross

df = load_data("AAPL", "5y")

bt = Backtest(
    df,
    SmaCross,
    cash=10000,
    commission=0.0005,
    trade_on_close=False
)

results = bt.run(
    n1=10,
    n2=20,
    SL=None,   # stop loss (เช่น 0.05)
    TP=None    # take profit (เช่น 0.10)
)

print(results)
bt.plot()
