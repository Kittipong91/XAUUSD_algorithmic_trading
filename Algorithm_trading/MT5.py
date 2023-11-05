from datetime import datetime
import pandas as pd
import MetaTrader5 as mt5

class MT5:
   def get_data(symbol, n, timeframe):       
        mt5.initialize()
        utc_from = datetime.now()
        rates = mt5.copy_rates_from(symbol, timeframe, utc_from, n)
        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time']+25200, unit='s')
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], format='%Y-%m-%d')
        rates_frame = rates_frame.set_index('time')
        return rates_frame

   def orders(symbol, lot, buy=True, id_position=None, TP=0.01 , SL=0.01):
       mt5.initialize()
       #filling_mode = mt5.symbol_info(symbol).filling_mode - 1
       filling_mode =  mt5.ORDER_FILLING_IOC
       ask_price = mt5.symbol_info_tick(symbol).ask
       bid_price = mt5.symbol_info_tick(symbol).bid
       deviation = 20  # mt5.getSlippage(symbol)
       # **************************** Open a trade *****************************
       if id_position == None:
           # Buy order Parameters
           if buy:
               type_trade = mt5.ORDER_TYPE_BUY
               sl = ask_price*(1-SL)
               tp = ask_price*(1+TP)
               price = ask_price
           # Sell order Parameters
           else:
               type_trade = mt5.ORDER_TYPE_SELL
               sl = bid_price*(1+SL)
               tp = bid_price*(1-TP)
               price = bid_price
           # Open the trade
           request = {
               "action": mt5.TRADE_ACTION_DEAL,
               "symbol": symbol,
               "volume": lot,
               "type": type_trade,
               "price": price,
               "deviation": deviation,
               "sl": sl,
               "tp": tp,
               "magic": 234000,
               "comment": "python script order",
               "type_time": mt5.ORDER_TIME_GTC,
               "type_filling": filling_mode,
           }
           # send a trading request
           result = mt5.order_send(request)
           result_comment = result.comment

       # **************************** Close a trade *****************************
       else:
           # Buy order Parameters
           if buy:
               type_trade = mt5.ORDER_TYPE_SELL
               
               price = bid_price

           # Sell order Parameters
           else:
               type_trade = mt5.ORDER_TYPE_BUY
               price = ask_price

           # Close the trade
           request = {
               "action": mt5.TRADE_ACTION_DEAL,
               "symbol": symbol,
               "volume": lot,
               "type": type_trade,
               "position": id_position,
               "price": price,
               "deviation": deviation,
               "magic": 234000,
               "comment": "python script order",
               "type_time": mt5.ORDER_TIME_GTC,
               "type_filling": filling_mode,
           }

           # send a trading request
           result = mt5.order_send(request)
           result_comment = result.comment
       return result.comment

   def resume():
      mt5.initialize()
      colonnes = ["ticket", "position", "symbol", "volume"]
      current = mt5.positions_get()
      summary = pd.DataFrame()
      for element in current:
           element_pandas = pd.DataFrame([element.ticket,
                                          element.type,
                                          element.symbol,
                                          element.volume],
                                         index=colonnes).transpose()
           summary = pd.concat((summary, element_pandas), axis=0)

      return summary


   def run(symbol, long, short, lot, tp=0.01, sl=0.01):
        
        TP = tp
        SL = sl
        mt5.initialize()
        print("------------------------------------------------------------------")
        print("Date: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("SYMBOL:", symbol)
        current_open_positions = MT5.resume()
        print(f"BUY: {long} \t  SHORT: {short}")
  
        try:
            position = current_open_positions.loc[current_open_positions["symbol"]==symbol].values[0][1]

            identifier = current_open_positions.loc[current_open_positions["symbol"]==symbol].values[0][0]
        except:
            position= None
            identifier = None

        print(f"POSITION: {position} \t ID: {identifier}")

        # Close trades
        if long==True and position==0:
            long=False

        elif long==False and position==0:
            res = MT5.orders(symbol, lot, buy=True, id_position=identifier, TP=TP ,SL=SL)
            print(f"CLOSE LONG TRADE: {res}")

        elif short==True and position ==1:
            short=False

        elif short == False and position == 1:
            res = MT5.orders(symbol, lot, buy=False, id_position=identifier, TP=TP ,SL=SL)
            print(f"CLOSE SHORT TRADE: {res}")

        else:
            pass


        """ Buy or short """
        if long==True:

            res = MT5.orders(symbol, lot, buy=True, id_position=None , TP=TP ,SL=SL) 
           
            print(f"OPEN LONG TRADE: {res}")

        if short==True:
            res = MT5.orders(symbol, lot, buy=False, id_position=None, TP=TP ,SL=SL)
          
            print(f"OPEN SHORT TRADE: {res}")

        print("------------------------------------------------------------------")

   def close_all_orders():
        mt5.initialize()
        result = MT5.resume()
        for i in range(len(result)):
            row = result.iloc[0+i:1+i,:]
            if row["position"][0]==0:
                MT5.orders(row["symbol"][0], row["volume"][0], buy=True, id_position=row["ticket"][0])

            else:
                MT5.orders(row["symbol"][0], row["volume"][0], buy=False, id_position=row["ticket"][0])

