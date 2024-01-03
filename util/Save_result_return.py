import pandas as pd

def save_to_csv(df, file_path, include_index=False):
    equity_curve = df['_equity_curve'].copy()
    equity_df = pd.DataFrame(equity_curve, columns=['Equity'])
    equity_df['returns'] = equity_df['Equity'].pct_change().fillna(0)
    equity_df = equity_df.drop('Equity', axis=1)
    equity_df.to_csv(file_path, index=True)
   
