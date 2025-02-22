import pandas as pd
import config


class TradeEngine:

    def __init__(self) -> None:
        self.open_orders = []
        self.open_positions = []
        self.trade_list = []

        self.close_price = None
        self.high_price = None
        self.low_price = None
        self.csv_template = None

    def save_trade_report(self):
        """
            Get all Trade and save them in a Csv file
        """
        self.csv_template = pd.DataFrame(
            columns=['symbol', 'order_status', 'position_status', 'side', 'enter_price',
                     'stop_loss', 'take_profit', 'volume', 'commission', 'unrealized_profit_loss',
                     'realized_profit_loss', 'close_price', 'trade_status',
                     'realized_profit_loss_percent', 'final_volume'])
        for trade in self.trade_list:
            self.csv_template = self.csv_template.append(trade, ignore_index=True)

        self.csv_template.to_csv(config.report_path)

    def clean_all(self):
        """
            clean all Open orders / open positions / trade history
        """
        self.open_orders = []
        self.open_positions = []
        self.trade_list = []

    def clean_all_orders(self):
        """
            clean all open orders
        """
        self.open_orders = []

    def check_orders(self, high, low, close):
        """
            Check all Limit orders with every candle and if executed it wil be known as a position
        """

        for order in self.open_orders:

            if order["order_status"] != "BadOrdering(10001)":

                enter_price = float(order["enter_price"])
                side = order["side"]

                if order["order_type"] == "limit":
                    if low <= enter_price <= high:
                        self.execute_limit_order(order)

                    if side == "long":
                        if low < enter_price:
                            order["order_status"] = "BadOrdering(10001)"
                    if side == "short":
                        if high > enter_price:
                            order["order_status"] = "BadOrdering(10001)"

    def check_positions(self, high, low, close):
        """
            Check all open positions with every candle and if closed it wil be known as a Trade in Trade History
        """
        for position in self.open_positions:
            sl = float(position["stop_loss"])
            tp = float(position["take_profit"])
            enter_price = float(position["enter_price"])
            side = position["side"]

            if side == "long":

                # check if Stop loss Take profit hit
                if low <= sl <= high or low < sl:
                    position["unrealized_profit_loss"] =0
                    self.close_position(position=position, closed_price=sl)
                elif low <= tp <= high or high > tp:
                    position["unrealized_profit_loss"] = 0
                    self.close_position(position=position, closed_price=tp)
                else:
                    # check unrealized profit status
                    position["unrealized_profit_loss"] = round((close - enter_price) /enter_price * 100, 2)

            if side == "short":
                # check unrealized profit status

                # check if Stop loss Take profit hit
                if low <= sl <= high or high > sl:
                    position["unrealized_profit_loss"] = 0
                    self.close_position(position=position, closed_price=sl)
                elif low <= tp <= high or low < tp:
                    position["unrealized_profit_loss"] = 0
                    self.close_position(position=position, closed_price=tp)
                else:
                    # check unrealized profit status
                    position["unrealized_profit_loss"] = round((enter_price - close) / enter_price * 100, 2)

    def place_market_order(self, symbol: str, entry_price: float, sl: float, tp: float, volume: float,
                           commission: float, side: str) -> None:
        """
        it uses for placing a market order (this order will be executed at entry price,
        entry price is close price of current candle)
        """
        position = {
            "symbol": f"{symbol}",
            "order_status": "executed",
            "position_status": "open",
            "order_type": "market",
            "side": f"{side}",
            "enter_price": f"{entry_price}",
            "stop_loss": f"{sl}",
            "take_profit": f"{tp}",
            "close_volume": f"0",
            "volume": f"{volume}",
            "commission": f"{commission}",
            "unrealized_profit_loss": "",
            "realized_profit_loss": "",
            "close_price": "",
            "trade_status": "",  # sl_hit, tp_hit, closed
            "realized_profit_loss_percent": "",
            "final_volume": "",
        }

        self.open_positions.append(position)

    def place_limit_order(self, symbol: str, entry_price: float, sl: float, tp: float, volume: float,
                          commission: float, side: str):
        """
            it uses for placing a Limit Order (this order will be executed when price arrived to entry price)
            Notice1 : BadOrdering(10001)
                    it's status of order that we can't execute them because they are not Limit order anymore
                    Limit Order side Long:
                        Bad Condition:
                            current price < Enter price
                        if price is under enter price we can't execute this order, and we know this as bad order

                    Limit Order side short:
                        Bad Condition:
                            current price > Enter price
                        if price is upper enter price we can't execute this order, and we know this as bad order

        """
        order = {
            "symbol": f"{symbol}",
            "order_status": "open",
            "position_status": "NotExecuted",
            "order_type": "limit",
            "side": f"{side}",
            "enter_price": f"{entry_price}",
            "stop_loss": f"{sl}",
            "take_profit": f"{tp}",
            "volume": f"{volume}",
            "commission": f"{commission}",
            "unrealized_profit_loss": "",
            "realized_profit_loss": "",
            "close_price": "",
            "trade_status": "",  # sl_hit, tp_hit, closed
            "realized_profit_loss_percent": "",
            "final_volume": "",
        }
        self.open_orders.append(order)

    def execute_limit_order(self, order):
        """
            it uses for executing limit orders (it changes an order to position)
        """
        # remove from open orders
        if order["order_status"] != "BadOrdering(10001)":
            self.open_orders.remove(order)

            order["order_status"] = "executed"
            order["position_status"] = "open"
            # add to open positions
            self.open_positions.append(order)

    def calculate_account_loss_profit(self, account_balance):
        """
            Get all Trade and add profits or losses to account balance
        """
        for trade in self.trade_list:
            account_balance += round(float(trade["realized_profit_loss"]), 2)

        return account_balance

    def close_all_positions(self, closed_price):
        """
            Get all open positions and close them
        """
        for position in self.open_positions:
            self.close_position(position=position, closed_price=closed_price)
            
    def calculate_trade_data(self, volume, price1, price2):
        realized_profit_loss = round(volume * (price1 - price2) / price2, 2)
        realized_profit_loss_percent = round((price1 - price2) / price2 * 100, 2)
        final_volume = round(volume + volume * (price1 - price2) / price2, 2)

        return realized_profit_loss, realized_profit_loss_percent, final_volume

    def handle_trade_update(self, position, trade_status, volume, price1, price2):
        position["trade_status"] = trade_status
        position["realized_profit_loss"], position["realized_profit_loss_percent"], position["final_volume"] = self.calculate_trade_data(volume, price1, price2)
        
        return position

    def close_single_position(self, position, closed_price):
        """
        Closes an open position and writes into trade history.
        """
        position["position_status"] = "closed"
        position["close_price"] = closed_price
        position["unrealized_profit_loss"] = 0

        # Extracting position details
        entry_price = float(position["enter_price"])
        stop_loss = float(position["stop_loss"])
        take_profit = float(position["take_profit"])
        volume = float(position["volume"])
        side = str(position["side"])

        if side == "long":
            if closed_price == stop_loss:
                position = self.handle_trade_update(position, "sl_hit", volume, stop_loss, entry_price)

            elif closed_price == take_profit:
                position = self.handle_trade_update(position, "tp_hit", volume, take_profit, entry_price)

            else:
                position = self.handle_trade_update(position, "closed", volume, closed_price, entry_price)

        elif side == "short":
            if closed_price == stop_loss:
                position = self.handle_trade_update(position, "sl_hit", volume, entry_price, stop_loss)

            elif closed_price == take_profit:
                position = self.handle_trade_update(position, "tp_hit", volume, entry_price, take_profit)

            else:
                position = self.handle_trade_update(position, "closed", volume, entry_price, closed_price)

        self.trade_list.append(position)



    def close_position(self, position, closed_price, closed_volume=None):


        """
            closing open position and write into trade history .
        """
        # Extracting position details
        entry_price = float(position["enter_price"])
        volume = float(position["volume"])
        
        if closed_volume is None:
            closed_volume = volume

        # Check if the closed_volume is greater than the position volume
        if closed_volume > volume:
            print(f"Closed volume {closed_volume} is greater than the position volume {volume}")
            return

        if closed_volume < volume:
            position["volume"] = str(volume - closed_volume)
            position["close_volume"] = str(float(position["close_volume"]) + closed_volume)
            position["unrealized_profit_loss"] = round(float(position["volume"]) * (closed_price - entry_price) / entry_price, 2)
        else:
            self.open_positions.remove(position)

        closed_position = position.copy()
        closed_position["volume"] = str(closed_volume)
            
        self.close_single_position(closed_position, closed_price)