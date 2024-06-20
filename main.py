import pandas as pd
from utils.config_loader import load_config
from core.run_bot import bot_run

run_mode = ['live', 'demo']

def execute_strategies():
    # Load the configuration based on the provided run mode
    config = load_config(strategies_run_mode=run_mode)

    for strategy_name, settings in config.items():
        # Use the settings for each strategy to make trading decisions
        print(f"Executing {strategy_name} with symbols: {settings['symbols']} timeframe: {settings['timeframe']}")
    return config

if __name__ == "__main__":
    strategies = execute_strategies()
    bot_run(strategies)
    


""" testing*******


    # Example: Access the configuration for the 'TrendFollowing' strategy
    config = load_config(strategies_run_mode=run_mode)
    trend_following_config = pd.DataFrame([config.get('TrendFollowing', {})])
    print(trend_following_config)

    # Convert all strategies' configurations to a DataFrame
    strategies_df = pd.DataFrame.from_dict(config, orient='index')
    print(strategies_df)
"""