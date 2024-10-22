"""Some oftet used var\func"""
# import from parent dir
import os
import sys
# from pathlib import Path
# file = Path(__file__).resolve()
# package_root_directory = file.parents[1]
# sys.path.append(str(package_root_directory))
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
# --------------------------------------------------------#

# Project dir
project_path = Path(__file__).parent
sep = os.sep

# symbol_list = ['APTUSDT', "ETHUSDT", 'GMTUSDT', 'BNBUSDT', 'APEUSDT','GRTUSDT','MANAUSDT','SOLUSDT','BAKEUSDT','NEOUSDT',
#     'ETCUSDT','GALUSDT','UNFIUSDT','LINKUSDT','SUSHIUSDT','DYDXUSDT','REEFUSDT','DGBUSDT','XRPUSDT','DUSKUSDT', 'CELRUSDT',
# 'FILUSDT', 'XRPUSDT', 'MATICUSDT', 'CHZUSDT', 'SANDUSDT', 'ATOMUSDT', 'NEARUSDT']

TICKERS = [
    "APTUSDT",
    "ADAUSDT",
    "ETHUSDT",
    "GMTUSDT",
    "BNBUSDT",
    "APEUSDT",
    "GRTUSDT",
    "MANAUSDT",
    "SOLUSDT",
    "BAKEUSDT",
    "NEOUSDT",
    "ETCUSDT",
    "GALUSDT",
    "LINKUSDT",
    "DYDXUSDT",
    "DGBUSDT",
    "XRPUSDT",
    "DUSKUSDT",
    "CELRUSDT",
    "FILUSDT",
    "XRPUSDT",
    "MATICUSDT",
    "CHZUSDT",
    "SANDUSDT",
    "ATOMUSDT",
    "NEARUSDT",
    "CFXUSDT",
    "SXPUSDT",
    "BAKEUSDT",
    "AGIXUSDT",
    "ARBUSDT",
    "MASKUSDT",
    "DOGEUSDT",
    "LQTYUSDT",
    "C98USDT",
    "MAGICUSDT",
    "RNDRUSDT",
    'INJUSDT',
    'DOGEUSDT',
    'BCHUSDT',
    'WLDUSDT',
    'CYBERUSDT',
    'TRBUSDT',
    'XAIUSDT',
    'BNTUSDT',
    'MEMEUSDT',
    'ORDIUSDT',
    'POWRUSDT',
    'TIAUSDT',
    'PEOPLEUSDT',
    'SEIUSDT',
    'SUIUSDT',
    'GASUSDT',
    'ACEUSDT',
    'RADUSDT',
    'AAVEUSDT',
    'OPUSDT',
    'AVAXUSDT',
    'DOTUSDT',
    'ENSUSDT'
    ]



# TICKERS = [
#     "NEARUSDT",
#     "CFXUSDT",
#     "SXPUSDT",
#     "BAKEUSDT",
#     "AGIXUSDT",
#     "ARBUSDT",
#     "MASKUSDT",
#     "APTUSDT",
#     "GMTUSDT",
#     "BNBUSDT"

# ]


pairs_count = len(TICKERS) + 1  # +1(BTCUSDT from kline_api\kline_update)

# INTERVAL = ["1m", "5m", "30m", "1h", "4h"]

INTERVAL = ["1m", "5m"]

final_bars_spot = {f"{k}": 0 for k in INTERVAL}
final_bars_future = {f"{k}": 0 for k in INTERVAL}

trade_stream_status = {f"{k}": 0 for k in TICKERS}







