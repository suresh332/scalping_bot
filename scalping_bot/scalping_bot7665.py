import os
print("Current working directory:", os.getcwd())
print("Files in this directory:", os.listdir())

import time
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from tensorflow.keras.models import load_model
import pickle

# === CONFIG ===
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M15
lookback = 10

# Columns we care about
feature_cols = ['open', 'high', 'low', 'close', 'tick_volume']

# === INIT MT5 ===
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# === LOAD YOUR TRAINED MODEL & SCALER ===
try:
    model = load_model('scalping_model_high_low.h5', compile=False)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    mt5.shutdown()
    quit()

# === HELPER FUNCTIONS ===
def get_last_n_candles(n=lookback):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    if rates is None:
        return None
    return pd.DataFrame(rates)[feature_cols]

def wait_for_new_candle():
    last_time = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)[0]['time']
    while True:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
        if rates is None:
            time.sleep(1)
            continue
        current_time = rates[0]['time']
        if current_time != last_time:
            return pd.DataFrame(rates)[feature_cols]
        time.sleep(1)

# === INIT BUFFER ===
buffer_df = get_last_n_candles()
if buffer_df is None or len(buffer_df) < lookback:
    print(f"Failed to get initial {lookback} candles. Exiting.")
    mt5.shutdown()
    quit()

print(f"{pd.Timestamp.now()} → Bot started. Waiting for new candles...")

# === MAIN LOOP ===
while True:
    new_candle_df = wait_for_new_candle()
    buffer_df = pd.concat([buffer_df.iloc[1:], new_candle_df], ignore_index=True)

    # Scale buffer
    buffer_scaled = scaler.transform(buffer_df[feature_cols])
    X_live = buffer_scaled.reshape(1, lookback, len(feature_cols))

    # Get predictions
    future_high_pred, future_low_pred = model.predict(X_live, verbose=0)[0]
    current_close = buffer_df.iloc[-1]['close']

    # Print predicted values
    print(
        f"{pd.Timestamp.now()} → predicted_high={future_high_pred:.5f}, "
        f"predicted_low={future_low_pred:.5f}, close={current_close:.5f}"
    )
