import time
import datetime
import xlwings as xw 
from zerodha_api import kite_client as kite
import Functionsbasefile as bf 
# from datetime import datetime , timedelta
import pandas as pd 

''' Need to create a bracket order covering
Buying order condition,
Stop loss,
Target,
Exit at 14:55
Profit and loss.'''

stock_name = "RELIANCE"
qty = 1
structure = {'BUY_LTP': None, 'Order_no' : None, 'Buy_Traded': None,'Stop_Loss': None,'Target': None,'Time': None, 'Sell_LTP': None, 'Sell_Traded' : None,'pnl': None, 'Remark' : None}
sl = 0.020
Tgt =  0.040
ext_time = 14.55
current_time = datetime.datetime.now().time()

while True:
	ltp = bf.LTP(stock_name)
	openn = bf.OPENN(stock_name)
	if (ltp >= openn) and structure['Buy_Traded'] is None:
		Buy_order_placed = kite.place_order(variety = kite.VARIETY_AMO , exchange = kite.EXCHANGE_NSE , tradingsymbol = stock_name , transaction_type = kite.TRANSACTION_TYPE_BUY , quantity = qty , product = kite.PRODUCT_MIS , order_type = kite.ORDER_TYPE_MARKET , price = None, tag="Algo_Trade")
		print(f" Buy Order Placed {Buy_order_placed}")
		structure['BUY_LTP'] = ltp
		structure['Order_no'] = Buy_order_placed
		structure['Buy_Traded'] = "YES"
		structure['Stop_Loss'] = (ltp - sl*ltp)
		structure['Target'] = (ltp + Tgt*ltp)
		structure['Time'] = str(datetime.datetime.now().time())[:8]

	if structure['Buy_Traded'] == "YES" and structure['Sell_Traded'] is None:

		if ltp > structure['Target'] or ltp < structure['Stop_Loss'] or current_time == ext_time :
			Sell_order_placed = kite.place_order(variety = kite.VARIETY_AMO , exchange = kite.EXCHANGE_NSE , tradingsymbol = stock_name , transaction_type = kite.TRANSACTION_TYPE_SELL , quantity = qty , product = kite.PRODUCT_MIS , order_type = kite.ORDER_TYPE_MARKET , price = ltp, tag="Algo_Trade")
			print(Sell_order_placed)
			structure['Sell_LTP'] = ltp
			structure['Sell_Traded'] = "YES"
			structure['pnl'] = (structure['Sell_LTP'] - structure['BUY_LTP']) * qty
			if (ltp < structure['Stop_loss']):

					structure['Remark'] = 'StopLoss_Hit'



			if (ltp > structure['Target']):

					structure['Remark'] = 'Target_Hit'

					print(pnl)
	
