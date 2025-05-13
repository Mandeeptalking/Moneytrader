INDICATOR_CATALOG = {
    "RSI": {
        "pandas_ta": "rsi",
        "settings": [
            {"name": "Period", "key": "length", "default": 14},
            {"name": "MA Period", "key": "maPeriod", "default": 10}
        ],
        "components": ["RSI", "RSI_MA", "OVERBOUGHT", "OVERSOLD"],
        "static_values": {
            "OVERBOUGHT": 70,
            "OVERSOLD": 30,
            "MIDDLE": 50
        },
        "compare_options": ["value", "indicator_component"]
    },
    "MACD": {
        "pandas_ta": "macd",
        "settings": [
            {"name": "Fast Period", "key": "fast", "default": 12},
            {"name": "Slow Period", "key": "slow", "default": 26},
            {"name": "Signal Period", "key": "signal", "default": 9}
        ],
        "components": ["MACD_LINE", "SIGNAL_LINE", "HISTOGRAM", "ZERO_LINE"],
        "static_values": {"ZERO_LINE": 0},
        "compare_options": ["value", "indicator_component"]
    },
    "EMA": {
        "pandas_ta": "ema",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["EMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "SMA": {
        "pandas_ta": "sma",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["SMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "BB": {
        "pandas_ta": "bbands",
        "settings": [
            {"name": "Period", "key": "length", "default": 20},
            {"name": "Standard Deviations", "key": "std", "default": 2}
        ],
        "components": ["UPPER", "LOWER", "MIDDLE", "BANDWIDTH", "PERCENT_B"],
        "compare_options": ["value", "indicator_component"]
    },
    "VOLUME": {
        "pandas_ta": "volume",
        "settings": [
            {"name": "MA Period", "key": "maPeriod", "default": 20},
            {"name": "RVOL Lookback", "key": "rvolPeriod", "default": 20}
        ],
        "components": ["VOLUME", "VOLUME_MA", "RVOL", "VOLUME_DELTA"],
        "compare_options": ["value", "indicator_component"]
    },
    "PVO": {
        "pandas_ta": "pvo",
        "settings": [
            {"name": "Fast Period", "key": "fast", "default": 12},
            {"name": "Slow Period", "key": "slow", "default": 26},
            {"name": "Signal Period", "key": "signal", "default": 9}
        ],
        "components": ["PVO_LINE", "PVO_SIGNAL_LINE", "ZERO_LINE"],
        "static_values": {
            "ZERO_LINE": 0
        },
        "compare_options": ["value", "indicator_component"]
    },
    "VOLUME_SPIKE": {
        "pandas_ta": None,
        "settings": [
            {"name": "Volume MA Period", "key": "maPeriod", "default": 20},
            {"name": "Spike Multiplier", "key": "multiplier", "default": 2.0}
        ],
        "components": ["VOLUME", "VOLUME_MA", "VOLUME_SPIKE"],
        "compare_options": ["value", "indicator_component"]
    },
    "ADX": {
        "pandas_ta": "adx",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["ADX", "PLUS_DI", "MINUS_DI"],
        "compare_options": ["value", "indicator_component"]
    },
    "ATR": {
        "pandas_ta": "atr",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["ATR"],
        "compare_options": ["value", "indicator_component"]
    },
    "OBV": {
        "pandas_ta": "obv",
        "settings": [],
        "components": ["OBV"],
        "compare_options": ["value", "indicator_component"]
    },
    "CCI": {
        "pandas_ta": "cci",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["CCI"],
        "compare_options": ["value", "indicator_component"]
    },
    "MFI": {
        "pandas_ta": "mfi",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["MFI"],
        "compare_options": ["value", "indicator_component"]
    },
    "Williams %R": {
        "pandas_ta": "willr",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["WILLR"],
        "compare_options": ["value", "indicator_component"]
    },
    "Stochastic Oscillator": {
        "pandas_ta": "stoch",
        "settings": [
            {"name": "K Period", "key": "k", "default": 14},
            {"name": "D Period", "key": "d", "default": 3},
            {"name": "Smooth K", "key": "smooth_k", "default": 3}
        ],
        "components": ["STOCH_K", "STOCH_D"],
        "compare_options": ["value", "indicator_component"]
    },
    "Stochastic RSI": {
        "pandas_ta": "stochrsi",
        "settings": [
            {"name": "RSI Period", "key": "length", "default": 14},
            {"name": "Stochastic Period", "key": "stoch_length", "default": 14},
            {"name": "Smooth K", "key": "smooth_k", "default": 3},
            {"name": "Smooth D", "key": "smooth_d", "default": 3}
        ],
        "components": ["STOCHRSI_K", "STOCHRSI_D"],
        "compare_options": ["value", "indicator_component"]
    },
    "Ultimate Oscillator": {
        "pandas_ta": "uo",
        "settings": [
            {"name": "Short Period", "key": "short", "default": 7},
            {"name": "Medium Period", "key": "medium", "default": 14},
            {"name": "Long Period", "key": "long", "default": 28}
        ],
        "components": ["UO"],
        "compare_options": ["value", "indicator_component"]
    },
    "ROC": {
        "pandas_ta": "roc",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["ROC"],
        "compare_options": ["value", "indicator_component"]
    },
    "Chaikin Money Flow (CMF)": {
        "pandas_ta": "cmf",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["CMF"],
        "compare_options": ["value", "indicator_component"]
    },
    "VWAP": {
        "pandas_ta": "vwap",
        "settings": [],
        "components": ["VWAP"],
        "compare_options": ["value", "indicator_component"]
    },
    "Ichimoku Cloud": {
        "pandas_ta": "ichimoku",
        "settings": [
            {"name": "Tenkan Period", "key": "tenkan", "default": 9},
            {"name": "Kijun Period", "key": "kijun", "default": 26},
            {"name": "Senkou Span B Period", "key": "senkou", "default": 52}
        ],
        "components": [
            "TENKAN_SEN",
            "KIJUN_SEN",
            "SENKOU_SPAN_A",
            "SENKOU_SPAN_B",
            "CHIKOU_SPAN"
        ],
        "compare_options": ["value", "indicator_component"]
    },
    "TSI": {
        "pandas_ta": "tsi",
        "settings": [
            {"name": "Short Length", "key": "short", "default": 13},
            {"name": "Long Length", "key": "long", "default": 25}
        ],
        "components": ["TSI"],
        "compare_options": ["value", "indicator_component"]
    },
    "PPO": {
        "pandas_ta": "ppo",
        "settings": [
            {"name": "Fast Period", "key": "fast", "default": 12},
            {"name": "Slow Period", "key": "slow", "default": 26},
            {"name": "Signal Period", "key": "signal", "default": 9}
        ],
        "components": ["PPO_LINE", "PPO_SIGNAL_LINE", "ZERO_LINE"],
        "static_values": {"ZERO_LINE": 0},
        "compare_options": ["value", "indicator_component"]
    },
    "DPO": {
        "pandas_ta": "dpo",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["DPO"],
        "compare_options": ["value", "indicator_component"]
    },
    "Donchian Channels": {
        "pandas_ta": "donchian",
        "settings": [
            {"name": "Lookback Period", "key": "lookback", "default": 20}
        ],
        "components": ["DONCHIAN_UPPER", "DONCHIAN_LOWER", "DONCHIAN_MID"],
        "compare_options": ["value", "indicator_component"]
    },
    "Keltner Channels": {
        "pandas_ta": "kc",
        "settings": [
            {"name": "EMA Period", "key": "ema", "default": 20},
            {"name": "ATR Period", "key": "atr", "default": 10},
            {"name": "Multiplier", "key": "mult", "default": 2}
        ],
        "components": ["KC_UPPER", "KC_LOWER", "KC_MID"],
        "compare_options": ["value", "indicator_component"]
    },
    "SuperTrend": {
        "pandas_ta": "supertrend",
        "settings": [
            {"name": "ATR Period", "key": "length", "default": 10},
            {"name": "Multiplier", "key": "multiplier", "default": 3.0}
        ],
        "components": ["SUPERTREND"],
        "compare_options": ["value", "indicator_component"]
    },
    "PSAR": {
        "pandas_ta": "psar",
        "settings": [
            {"name": "Step", "key": "step", "default": 0.02},
            {"name": "Max Step", "key": "max_step", "default": 0.2}
        ],
        "components": ["PSAR"],
        "compare_options": ["value", "indicator_component"]
    },
    "TRIX": {
        "pandas_ta": "trix",
        "settings": [
            {"name": "Period", "key": "length", "default": 15}
        ],
        "components": ["TRIX"],
        "compare_options": ["value", "indicator_component"]
    },
    "Vortex Indicator": {
        "pandas_ta": "vi",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["VI_PLUS", "VI_MINUS"],
        "compare_options": ["value", "indicator_component"]
    },
    "Aroon Indicator": {
        "pandas_ta": "aroon",
        "settings": [
            {"name": "Period", "key": "length", "default": 25}
        ],
        "components": ["AROON_UP", "AROON_DOWN"],
        "compare_options": ["value", "indicator_component"]
    },
    "Coppock Curve": {
        "pandas_ta": "coppock",
        "settings": [],
        "components": ["COPPOCK"],
        "compare_options": ["value", "indicator_component"]
    },
    "Balance of Power (BOP)": {
        "pandas_ta": "bop",
        "settings": [],
        "components": ["BOP"],
        "compare_options": ["value", "indicator_component"]
    },
    "Elder’s Force Index (EFI)": {
        "pandas_ta": "efi",
        "settings": [
            {"name": "Period", "key": "length", "default": 13}
        ],
        "components": ["EFI"],
        "compare_options": ["value", "indicator_component"]
    },
    "Ease of Movement (EOM)": {
        "pandas_ta": "eom",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["EOM"],
        "compare_options": ["value", "indicator_component"]
    },
    "Relative Vigor Index (RVI)": {
        "pandas_ta": "rvi",
        "settings": [
            {"name": "Period", "key": "length", "default": 10}
        ],
        "components": ["RVI", "RVI_SIGNAL"],
        "compare_options": ["value", "indicator_component"]
    },
    "DMI": {
        "pandas_ta": "dmi",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["DMI_PLUS", "DMI_MINUS", "DX"],
        "compare_options": ["value", "indicator_component"]
    },
    "Chande Momentum Oscillator (CMO)": {
        "pandas_ta": "cmo",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["CMO"],
        "compare_options": ["value", "indicator_component"]
    },
    "Fisher Transform": {
        "pandas_ta": "fisher",
        "settings": [
            {"name": "Period", "key": "length", "default": 10}
        ],
        "components": ["FISHER", "FISHER_SIGNAL"],
        "compare_options": ["value", "indicator_component"]
    },
    "Know Sure Thing (KST)": {
        "pandas_ta": "kst",
        "settings": [
            {"name": "ROC1 Period", "key": "roc1", "default": 10},
            {"name": "ROC2 Period", "key": "roc2", "default": 15},
            {"name": "ROC3 Period", "key": "roc3", "default": 20},
            {"name": "ROC4 Period", "key": "roc4", "default": 30},
            {"name": "Signal Period", "key": "signal", "default": 9}
        ],
        "components": ["KST", "KST_SIGNAL"],
        "compare_options": ["value", "indicator_component"]
    },
    "Mass Index": {
        "pandas_ta": "mass",
        "settings": [
            {"name": "Period", "key": "length", "default": 25}
        ],
        "components": ["MASS"],
        "compare_options": ["value", "indicator_component"]
    },
    "Schaff Trend Cycle (STC)": {
        "pandas_ta": "stc",
        "settings": [
            {"name": "Short Cycle", "key": "short", "default": 23},
            {"name": "Long Cycle", "key": "long", "default": 50}
        ],
        "components": ["STC"],
        "compare_options": ["value", "indicator_component"]
    },
    "Donchian Width": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["DONCHIAN_WIDTH"],
        "compare_options": ["value", "indicator_component"]
    },
    "McGinley Dynamic": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["MCGINLEY"],
        "compare_options": ["value", "indicator_component"]
    },
    "Price ROC (PROC)": {
        "pandas_ta": "roc",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["PROC"],
        "compare_options": ["value", "indicator_component"]
    },
    "Fractal Indicator": {
        "pandas_ta": None,
        "settings": [],
        "components": ["FRACTAL_UP", "FRACTAL_DOWN"],
        "compare_options": ["value", "indicator_component"]
    },
    "Gopalakrishnan Range Index (GAPO)": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["GAPO"],
        "compare_options": ["value", "indicator_component"]
    },
    "Intraday Momentum Index (IMI)": {
        "pandas_ta": "imi",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["IMI"],
        "compare_options": ["value", "indicator_component"]
    },
    "STARC Bands": {
        "pandas_ta": "starc",
        "settings": [
            {"name": "SMA Period", "key": "sma_period", "default": 5},
            {"name": "ATR Period", "key": "atr_period", "default": 15},
            {"name": "Multiplier", "key": "multiplier", "default": 2}
        ],
        "components": ["STARC_UPPER", "STARC_LOWER"],
        "compare_options": ["value", "indicator_component"]
    },
    "VIDYA": {
        "pandas_ta": None,
        "settings": [
            {"name": "Short Period", "key": "short", "default": 12},
            {"name": "Long Period", "key": "long", "default": 26}
        ],
        "components": ["VIDYA"],
        "compare_options": ["value", "indicator_component"]
    },
    "Z-Score Indicator": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["ZSCORE"],
        "compare_options": ["value", "indicator_component"]
    },
    "Hull Moving Average (HMA)": {
        "pandas_ta": "hma",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["HMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "Zero Lag Moving Average (ZLMA)": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["ZLMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "Smoothed Moving Average (SMMA)": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["SMMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "Double Exponential Moving Average (DEMA)": {
        "pandas_ta": "dema",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["DEMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "Triple Exponential Moving Average (TEMA)": {
        "pandas_ta": "tema",
        "settings": [
            {"name": "Period", "key": "length", "default": 20}
        ],
        "components": ["TEMA"],
        "compare_options": ["value", "indicator_component"]
    },
    "Linear Regression Indicator": {
        "pandas_ta": "linreg",
        "settings": [
            {"name": "Period", "key": "length", "default": 14}
        ],
        "components": ["LINEAR_REGRESSION"],
        "compare_options": ["value", "indicator_component"]
    },
    "Gann HiLo Activator": {
        "pandas_ta": None,
        "settings": [
            {"name": "Period", "key": "length", "default": 10}
        ],
        "components": ["GANN_HILO"],
        "compare_options": ["value", "indicator_component"]
    }
}
