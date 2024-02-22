import pandas as pd

def save_to_csv(df, file_path, include_index=False):
    equity_curve = df['_equity_curve'].copy()
    equity_df = pd.DataFrame(equity_curve, columns=['Equity', 'DrawdownPct' , 'DrawdownDuration'])
    equity_df['returns'] = equity_df['Equity'].pct_change().fillna(0)
    equity_df.to_csv(file_path, index=True)

    trade = df['_trades'].copy()
    trade_df = pd.DataFrame(trade, columns=[
                            'Size', 'EntryBar', 'ExitBar', 'EntryPrice', 'ExitPrice', 'PnL', 'ReturnPct', 'EntryTime', 'ExitTime', 'Duration'])
    file_path_trade = file_path.replace('.csv', '_trade.csv')
    trade_df.to_csv(file_path_trade, index=True)

   
