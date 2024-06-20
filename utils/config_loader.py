import pandas as pd
import os

def get_timeframe_number(timeframe):
    # Mapping for the "timeframe" values to their respective 1000's digit
    timeframe_mapping = {
        'M1': 1000,
        'M5': 2000,
        'M15': 3000,
        'M30': 4000,
        'H1': 5000,
        'H4': 6000,
        'D1': 7000,
        'W1': 8000
    }
    
    # Return the corresponding number for the given timeframe, will retrun 0 by default = error (need to check)
    return timeframe_mapping.get(timeframe, 0)

def get_currency_magic_number(currency_pair):
    # Mapping for the "currency_pair" values to their respective magic numbers
    currency_mapping = {
        'AUDCAD': 1,
        'AUDCHF': 2,
        'AUDJPY': 3,
        'AUDNZD': 4,
        'AUDUSD': 5,
        'CADCHF': 6,
        'CADJPY': 7,
        'CHFJPY': 8,
        'EURAUD': 9,
        'EURCAD': 10,
        'EURCHF': 11,
        'EURGBP': 12,
        'EURJPY': 13,
        'EURNZD': 14,
        'EURUSD': 15,
        'GBPAUD': 16,
        'GBPCAD': 17,
        'GBPCHF': 18,
        'GBPJPY': 19,
        'GBPNZD': 20,
        'GBPUSD': 21,
        'NZDCAD': 22,
        'NZDCHF': 23,
        'NZDJPY': 24,
        'NZDUSD': 25,
        'USDCAD': 26,
        'USDCHF': 27,
        'USDJPY': 28,
        'GOLD': 40,
        'SILVER': 41,
        'SP500': 50,
        'Oil': 60,
        'Gas': 61
    }
    
    # Return the corresponding magic number for the given currency pair, will retrun 0 by default = error (need to check)
    return currency_mapping.get(currency_pair, 0)




def str_to_bool(s):
    """
    Convert a value to boolean.
    Handles both boolean and string representations of truthy/falsy values.
    
    Parameters:
        s (str or bool): The value to convert.

    Returns:
        bool: The converted boolean value.
    """
    if isinstance(s, bool):
        return s
    return str(s).lower() == 'true'

def safe_int_convert(value, default=0):
    """
    Safely convert a value to an integer.
    If conversion fails, return a default value.

    Parameters:
        value: The value to convert.
        default (int): The default value to return if conversion fails.

    Returns:
        int: The converted integer value or the default value.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float_convert(value, default=0.0):
    """
    Safely convert a value to a float.
    If conversion fails, return a default value.

    Parameters:
        value: The value to convert.
        default (float): The default value to return if conversion fails.

    Returns:
        float: The converted float value or the default value.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def load_config(filename='config.xlsx', sheet_name='config', strategies_run_mode=['live']):
    """
    Load configuration from an Excel file into a structured dictionary.
    This loader reads the specified sheet and processes each row into a dictionary.

    Parameters:
        filename (str): The name of the Excel file to read.
        sheet_name (str): The name of the sheet in the Excel file to read.
        strategies_run_mode (list): List of strategy statuses to load (e.g., ['live', 'demo']).

    Returns:
        dict: A dictionary containing strategy configurations.
    """
    # Construct the full path to the configuration file
    config_path = os.path.join(os.path.dirname(__file__), filename)
    
    # Read the specified sheet into a DataFrame
    df = pd.read_excel(config_path, sheet_name=sheet_name)

    # Initialize an empty dictionary to hold strategy configurations
    strategies = {}

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Filter strategies based on the run mode
        if row['strategy_status'] not in strategies_run_mode:
            continue
        
        # Extract strategy name and symbols
        strategy_name = row['strategy_name']
        symbols = row['symbols'].split(';')

        # Construct the strategy configuration dictionary
        strategy_config = {
            'strategy_num': safe_int_convert(row['strategy_num']),
            'magic_num': 50_000_000 + get_timeframe_number(row['strategy_num']), # base of magic number, still needs the currency for full number
            'strategy_status': row['strategy_status'],
            'symbols': symbols,
            'timeframe': row['timeframe'],
            'tradeP_risk': safe_float_convert(row['tradeP_risk']),
            'tradeP_max_trades': safe_int_convert(row['tradeP_max_trades']),
            'tradeP_hour_start': safe_int_convert(row['tradeP_hour_start']),
            'tradeP_hour_length': safe_int_convert(row['tradeP_hour_length']),
            'tradeP_long': str_to_bool(row['tradeP_long']),
            'tradeP_short': str_to_bool(row['tradeP_short']),
            'tradeP_method': row['tradeP_method'],
            'tradeP_limit_order_expiration_bars': safe_int_convert(row['tradeP_limit_order_expiration_bars']),
            'sl_method': row['sl_method'],
            'sl_param': safe_float_convert(row['sl_param']),
            'trail_method': row['trail_method'],
            'trail_param': safe_float_convert(row['trail_param']),
            'tp_method': row['tp_method'],
            'tp_param': safe_float_convert(row['tp_param']),
            'indicator': row['indicator'],
            'indicator_params': {
                'a': row['indicator_param_a'],
                'b': row['indicator_param_b'],
                'c': row['indicator_param_c'],
                'd': row['indicator_param_d'],
                'e': row['indicator_param_e'],
                'f': row['indicator_param_f'],
            },
            'exitP_daily_profit_close': str_to_bool(row['exitP_daily_profit_close']),
            'exitP_daily_profit_close_days': safe_int_convert(row['exitP_daily_profit_close_days']),
            'exitP_daily_close': str_to_bool(row['exitP_daily_close']),
            'exitP_daily_close_days': safe_int_convert(row['exitP_daily_close_days']),
            'exitP_bars_close': safe_int_convert(row['exitP_bars_close']),
            'barsP_pattern': row['barsP_pattern'],
            'barsP_pattern_count': safe_int_convert(row['barsP_pattern_count']),
            'barsP_1st_candle': row['barsP_1st_candle'],
            'barsP_2nd_candle': row['barsP_2nd_candle'],
            'barsP_3rd_candle': row['barsP_3rd_candle'],
            'barsP_higher_timeframe': row['barsP_higher_timeframe'],
            'barsP_higher_pattern': row['barsP_higher_pattern'],
            'barsP_higher_pattern_count': safe_int_convert(row['barsP_higher_pattern_count']),
            'barsP_higher_1st_candle': row['barsP_higher_1st_candle'],
            'barsP_higher_2nd_candle': row['barsP_higher_2nd_candle'],
            'barsP_higher_3rd_candle': row['barsP_higher_3rd_candle'],
            'barsP_lower_timeframe': row['barsP_lower_timeframe'],
            'barsP_lower_pattern': row['barsP_lower_pattern'],
            'barsP_lower_pattern_count': safe_int_convert(row['barsP_lower_pattern_count']),
            'barsP_lower_1st_candle': row['barsP_lower_1st_candle'],
            'barsP_lower_2nd_candle': row['barsP_lower_2nd_candle'],
            'barsP_lower_3rd_candle': row['barsP_lower_3rd_candle'],
            'filterP_max_prev_prec_candle': safe_float_convert(row['filterP_max_prev_prec_candle']),
            'filterP_min_prev_prec_candle': safe_float_convert(row['filterP_min_prev_prec_candle']),
            'filterP_Sun': str_to_bool(row['filterP_Sun']),
            'filterP_Mon': str_to_bool(row['filterP_Mon']),
            'filterP_Tue': str_to_bool(row['filterP_Tue']),
            'filterP_Wed': str_to_bool(row['filterP_Wed']),
            'filterP_Thur': str_to_bool(row['filterP_Thur']),
            'filterP_Fri': str_to_bool(row['filterP_Fri']),
            'filterP_Sat': str_to_bool(row['filterP_Sat']),
            'filterP_max_rsi_deviation': safe_float_convert(row['filterP_max_rsi_deviation']),
            'filterP_min_rsi_deviation': safe_float_convert(row['filterP_min_rsi_deviation']),
        }

        # Add the strategy configuration to the strategies dictionary
        strategies[strategy_name] = strategy_config

    return strategies


