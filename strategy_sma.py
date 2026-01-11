import pandas as pd
from backtesting import Strategy
from backtesting.lib import crossover


class SmaCross(Strategy):
    # ค่า default (เปลี่ยนได้ตอน optimize)
    n1 = 8   # short SMA window
    n2 = 20   # long SMA window

    SL = 0.05   # Stop loss เช่น 0.05 (5%)
    TP = 0.10   # Take profit เช่น 0.10 (10%)

    def init(self):
        close = pd.Series(self.data.Close)

        self.sma_short = self.I(lambda x: x.rolling(self.n1).mean(), close)
        self.sma_long  = self.I(lambda x: x.rolling(self.n2).mean(), close)

    def next(self):

        price = self.data.Close[-1]

        # -----------------------------
        #   1) Golden Cross → BUY
        # -----------------------------
        if crossover(self.sma_short, self.sma_long):
            # ถ้ามี short อยู่ให้ปิดก่อน (กันพลาด)
            if self.position.is_short:
                self.position.close()

            # ถ้ายังไม่ถือ long → buy
            if not self.position.is_long:
                self.buy()

        # -----------------------------
        #   2) Death Cross → CLOSE (ไม่ short)
        # -----------------------------
        elif crossover(self.sma_long, self.sma_short):
            if self.position:
                self.position.close()

        # -----------------------------
        #   3) Stop Loss / Take Profit
        # -----------------------------
        if self.position and (self.SL or self.TP):

            entry = self.position.entry_price

            # Stop Loss สำหรับ Long
            if self.SL and price <= entry * (1 - self.SL):
                self.position.close()

            # Take Profit สำหรับ Long
            if self.TP and price >= entry * (1 + self.TP):
                self.position.close()
