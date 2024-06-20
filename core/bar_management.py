


import MetaTrader5 as mt5
from datetime import datetime, timedelta

# Global variables
PreviousHour = -1
PreviousDay = -1
PreviousMinute = -1

# Dictionary to keep track of the previous bar time for each time frame
PreviousBars = {}

# Dictionary to map time frames to their corresponding timedelta values
time_frame_deltas = {
    'M1': timedelta(minutes=1),
    'M5': timedelta(minutes=5),
    'M15': timedelta(minutes=15),
    'M30': timedelta(minutes=30),
    'H1': timedelta(minutes=60),
    'H4': timedelta(minutes=240),
    'D1': timedelta(minutes=1_440),
    'W1': timedelta(minutes=10_080),
}

def is_new_bar(time_frame):
    """
    Check if a new bar has started for the given time frame.

    Parameters:
        time_frame (str): The time frame to check for new bars (e.g., '1m', '5m', '15m').

    Returns:
        bool: True if a new bar has started, False otherwise.
    """
    global PreviousBars

    current_time = datetime.now()

    # Get the corresponding timedelta for the time frame
    if time_frame not in time_frame_deltas:
        raise ValueError(f"Unsupported time frame: {time_frame}")

    time_delta = time_frame_deltas[time_frame]

    # Calculate the next expected bar time
    next_expected_time = PreviousBars.get(time_frame, current_time - time_delta) + time_delta

    if current_time >= next_expected_time:
        PreviousBars[time_frame] = current_time
        return True

    return False

def handle_new_bar(strategy_name):
    """
    Handle operations that should occur on a new bar.
    """
    print(f"Handling new bar for strategy: {strategy_name}")

def positions_total_for_symbol(symbol):
    """
    Count the total positions for a given symbol.
    """
    return len([pos for pos in mt5.positions_get() if pos.symbol == symbol])

def handle_open_positions(symbol):
    """
    Manage open positions for a symbol.
    """
    print(f"Handling open positions for {symbol}...")

def manage_sl(symbol):
    """
    Manage stop loss for a symbol if trailing is enabled.
    """
    print(f"Managing SL for {symbol}...")

def write_balance_performance_file():
    """
    Write balance performance diagnostics.
    """
    print("Writing balance performance file...")

def on_minute(strategies):
    global PreviousHour, PreviousDay

    current_time = datetime.now()

    for strategy_name, settings in strategies.items():
        if is_new_bar(settings['timeframe']):
            handle_new_bar(strategy_name)

            for symbol in settings['symbols']:
                if positions_total_for_symbol(symbol) > 0:
                    handle_open_positions(symbol)

                if settings.get('trail_method', False):
                    if positions_total_for_symbol(symbol) > 0:
                        manage_sl(symbol)

        if PreviousHour != current_time.hour or PreviousDay != current_time.day:
            write_balance_performance_file()
            PreviousHour = current_time.hour
            PreviousDay = current_time.day
