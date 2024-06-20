# open tasks:
"""
1. load specific account from mt5?

"""



from bar_management import on_minute
import MetaTrader5 as mt5
import schedule
import time
from datetime import datetime




def bot_run(strategies):
    # Initialize MetaTrader 5
    if not mt5.initialize():
        print("Initialize() failed, error code =", mt5.last_error())
        quit()


    # Schedule the on_minute function to run every minute
    schedule.every(1).minutes.do(on_minute, strategies=strategies)

    # Main loop to keep the script running
    while True:
        schedule.run_pending()  # Check if any scheduled tasks need to run
        time.sleep(1)           # Sleep for 1 second before checking again

    



