import akshare as ak


df = ak.stock_zh_a_daily(symbol="sh600519", adjust="qfq")
print(df)
df.to_csv("600519.csv")
