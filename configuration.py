# coding: utf-8"""This File contains configuration parameters"""# When you want to attack a village telgram user id is needed. But for security you won't to display Telegram user id in enemy list.# So by KEY and RECREATE_CODE you encode and decode Telegram user id when you need to display.KEY = 1000000000  # Use this parameter to encode Telegram user id before display.RECREATE_CODE = 999999 # Use this parameter to decode Telegram user id.DEBUG_MODE = FalseSleepTime = 10# Database ParametersDBCONFIG = {'host': '10.10.200.220', 'username': 'root', 'password': '1234', 'database': 'worldwar'}# Telegram has been filtered by come countries. If you are there SET USE_PROXY = True . If not SET USE_PROXY = FALSEUSE_PROXY = FalsePROXY_URL = "http://127.0.0.1:8118"