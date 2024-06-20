import MetaTrader5 as mt5

def handle_open_positions(symbol):
    print("Handling open positions")
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        return

    # Implement specific exit strategies based on conditions
    manage_daily_exit(symbol)

def manage_daily_exit(symbol):
    # Example of a daily exit strategy
    positions = mt5.positions_get(symbol=symbol)
    for position in positions:
        # Close position under certain conditions
        if condition_to_close(position):  # Define your condition
            mt5.order_send({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(symbol).bid if position.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
                "magic": position.magic,
                "comment": "Closing trade",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            })

def condition_to_close(position):
    # Example condition: Close if current price is lower than open price by a certain percentage
    current_price = mt5.symbol_info_tick(position.symbol).bid if position.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(position.symbol).ask
    return current_price < position.price_open * 0.99


def close_all_trades(direction, symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return

    for position in positions:
        if position.type == (mt5.POSITION_TYPE_BUY if direction == 1 else mt5.POSITION_TYPE_SELL):
            mt5.order_send({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(symbol).bid if position.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
                "magic": position.magic,
                "comment": "Auto close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            })

