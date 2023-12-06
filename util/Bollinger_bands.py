
def Bollinger_bands(df, window, std_mult):
    df['rolling_mean'] = df['Close'].rolling(window).mean()
    df['rolling_std'] = df['Close'].rolling(window).std()
    df['upper_band'] = df['rolling_mean'] + (df['rolling_std'] * std_mult)
    df['lower_band'] = df['rolling_mean'] - (df['rolling_std'] * std_mult)
    return df
