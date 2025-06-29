# scalping_bot
this lstm+cnn hybrid model that fetch the last candles and predict the high and low of next 5th candle
# ⚡ EURUSD Scalping Bot (LSTM-Based with MT5 Integration)

This project is a scalping bot designed for the EURUSD currency pair. It uses a trained LSTM model to predict the **high** and **low** of upcoming candles based on the **last 10 candles** of OHLC data. The bot fetches live 15-minute candles from MetaTrader 5 (MT5), preprocesses them using a saved scaler, and performs predictions using a pretrained model.

> ⚠️ This version of the bot **only predicts the high and low** — it does **not generate buy/sell signals** automatically.

---

## 📁 Project Files

| File                             | Description                                                             |
|----------------------------------|-------------------------------------------------------------------------|
| `lstm.ipynb`                     | Jupyter notebook used to train the LSTM model                           |
| `scalpingbot.py`                | Main bot script for live predictions using MT5                          |
| `scalping_model_low_high.h5`    | Trained LSTM model that outputs future high and low                     |
| `scaler.pkl`                    | Saved MinMaxScaler to normalize live OHLC data                          |

---

## 📦 Features

- 🕒 15-minute timeframe candles
- 🔄 Uses **last 10 candles** as input
- 🎯 Predicts **high and low** of the upcoming candle(s)
- 🔗 Integrated with **MetaTrader 5**
- 🤖 Continuously runs and prints predictions (can be extended to generate signals)

---

## ⚙️ Requirements

Install the necessary packages:

```bash
pip install pandas numpy tensorflow scikit-learn MetaTrader5
pandas
numpy
tensorflow
scikit-learn
MetaTrader5
pandas
✅ 1. Launch MetaTrader 5
Ensure MetaTrader 5 is:

Installed and open

Logged into a valid broker account

EURUSD chart is active

✅ 2. Run the Scalping Bot
python scalpingbot.py
What it does:

Connects to MT5

Fetches the last 10 candles

Normalizes the OHLC input using scaler.pkl

Predicts next high and low values

Prints them in the terminal (optional: log or store them)

🧠 Model Overview
Input shape: (10, 4) → last 10 OHLC candles

Output: Two values → predicted high and low

Model type: LSTM neural network

Trained in: lstm.ipynb

Saved as: scalping_model_low_high.h5

[INFO] Predicted High: 1.08945
[INFO] Predicted Low : 1.08713
⚠️ Disclaimer
This bot is intended for educational and research purposes. Predictions are not guaranteed to be accurate. Use at your own risk and do not trade with real money unless you've backtested thoroughly.

👨‍💻 Author
Built by purbia suresh
🔗 www.linkedin.com/in/suresh7665purbiya
